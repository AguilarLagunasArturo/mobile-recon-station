'''
Register map:	https://43zrtwysvxb2gf29r5o0athu-wpengine.netdna-ssl.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf
Datasheet:		https://43zrtwysvxb2gf29r5o0athu-wpengine.netdna-ssl.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf
'''

import smbus
import numpy as np

''' REGISTERS [links] '''
ADRS = 0x68

GYRO_CONF = 0x1B
ACC_CONF = 0x1C

GYRO_RANGES = [
	0x00,		# +/- 250  DEG/s
	0x01,		# +/- 500  DEG/s
	0x02,		# +/- 1000 DEG/s
	0x03		# +/- 2000 DEG/s
]

GYRO_SCALE = [
	131.0,		# LSB / (DEG/s)
	65.5,		# LSB / (DEG/s)
	32.8,		# LSB / (DEG/s)
	16.4		# LSB / (DEG/s)
]

ACC_RANGES = [
	0x00,		# +/- 2  g
	0x01,		# +/- 4  g
	0x02,		# +/- 8  g
	0x03		# +/- 16 g
]

ACC_SCALE = [
	16384.0,	# LSB/g
	8192.0,		# LSB/g
	4096.0,		# LSB/g
	2048.0		# LSB/g
]

ACC_X = 0x3B
ACC_Y = 0x3D
ACC_Z = 0x3F

GYRO_X = 0x43
GYRO_Y = 0x45
GYRO_Z = 0x47

PWR_MGMT_1 = 0x6B

bus = smbus.SMBus(1)

''' functions  '''
gyro_mode = 0
acc_mode = 0

def setup():
	bus.write_byte_data(ADRS, PWR_MGMT_1, 0x08)						# TEMP OFF
	bus.write_byte_data(ADRS, GYRO_CONF, GYRO_RANGES[gyro_mode])	# GYRO RANGE
	bus.write_byte_data(ADRS, ACC_CONF, ACC_RANGES[acc_mode])		# GYRO ACC

def read_address(address):
	h = bus.read_byte_data(ADRS, address)
	l = bus.read_byte_data(ADRS, address + 1)
	value = (h << 8) | l
	if value >= 0x8000: # value > 32768
		return - ( (65535 - value) + 1 )
		#return -(65535 - value) - 1
		#return value - 65536
	else:
		return value

def get_gyro():
	gyro_x = read_address(GYRO_X)
	gyro_y = read_address(GYRO_Y)
	gyro_z = read_address(GYRO_Z)

	gx = gyro_x/GYRO_SCALE[gyro_mode]
	gy = gyro_y/GYRO_SCALE[gyro_mode]
	gz = gyro_z/GYRO_SCALE[gyro_mode]

	return np.array([gx, gy, gz])

def get_acc():
	acc_x = read_address(ACC_X)
	acc_y = read_address(ACC_Y)
	acc_z = read_address(ACC_Z)

	ax = acc_x/ACC_SCALE[acc_mode]
	ay = acc_y/ACC_SCALE[acc_mode]
	az = acc_z/ACC_SCALE[acc_mode]

	return np.array([ax, ay, az])

def calibrate(iterations):
	a = np.array([0.0, 0.0, 0.0])
	w = np.array([0.0, 0.0, 0.0])
	for n in range(iterations):
		a = a + get_acc()
		w = w + get_gyro()
	return [a/iterations, w/iterations]

setup()

a_off, w_off = calibrate(1000)
while True:
	a = get_acc() - a_off
	w = get_gyro() - w_off
	print('acc\t', a)
	print('gyro\t', w)
	print()
