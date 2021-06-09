'''
Register map:	https://43zrtwysvxb2gf29r5o0athu-wpengine.netdna-ssl.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf
Datasheet:		https://43zrtwysvxb2gf29r5o0athu-wpengine.netdna-ssl.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf
'''

import smbus

''' CONSTANTS '''
ACC_SCALE_2G = 16384.0
GYRO_SCALE_250D = 250.0

''' REGISTERS [links] '''
ADRS = 0x68

ACC_CONF = 0x1C
GYRO_CONF = 0x1B

ACCEL_RANGE_2G = 0x00
GYRO_RANGE_250DEG = 0x00

ACC_Y = 0x3D
GYRO_Z = 0x47

PWR_MGMT_1 = 0x6B

''' functions  '''
bus = smbus.SMBus(1)

def setup():
	bus.write_byte_data(ADRS, PWR_MGMT_1, 0x08)
	bus.write_byte_data(ADRS, ACC_CONF, ACCEL_RANGE_2G)
	bus.write_byte_data(ADRS, GYRO_CONF, GYRO_RANGE_250DEG)

def read_address(address):
	h = bus.read_byte_data(ADRS, address)
	l = bus.read_byte_data(ADRS, address + 1)
	value = (h << 8) | low
	if value >= 0x8000: # value > 32768
		return - ( (65535 - value) + 1 )
		#return -(65535 - value) - 1
		#return value - 65536
	else:
		return value

def get_acc():
	acc_y = read_address(ACC_Y)
	ay = acc_y/ACC_SCALE_2G
	return ay

def get_gyro():
	gyro_z = read_address(GYRO_Z)
	gz = gyro_z/GYRO_SCALE_250D
	return gz

setup()
while True:
	a = get_acc()
	w = get_gyro()
	print(a, w)
