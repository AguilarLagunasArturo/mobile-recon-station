'''
Register map:	https://43zrtwysvxb2gf29r5o0athu-wpengine.netdna-ssl.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf
Datasheet:		https://43zrtwysvxb2gf29r5o0athu-wpengine.netdna-ssl.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf
'''

import smbus
import numpy as np

class MPU6050:
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
		0x00,		# +/- 2  g [m/s^2]
		0x01,		# +/- 4  g [m/s^2]
		0x02,		# +/- 8  g [m/s^2]
		0x03		# +/- 16 g [m/s^2]
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

	def __init__(self, gyro_mode=0, acc_mode=0):
		self.bus = smbus.SMBus(1)
		self.bus.write_byte_data(MPU6050.ADRS, MPU6050.PWR_MGMT_1, 0x08)							# 0x08 -> TEMP OFF
		self.bus.write_byte_data(MPU6050.ADRS, MPU6050.GYRO_CONF, MPU6050.GYRO_RANGES[gyro_mode])	# GYRO RANGE
		self.bus.write_byte_data(MPU6050.ADRS, MPU6050.ACC_CONF, MPU6050.ACC_RANGES[acc_mode])		# GYRO ACC

	def __read_address(self, address):
		h = bus.read_byte_data(MPU6050.ADRS, address)
		l = bus.read_byte_data(MPU6050.ADRS, address + 1)
		value = (h << 8) | l

		# get signed value from mpu6050
		if value >= 0x8000: # value > 32768
			return - ( (65535 - value) + 1 )
			#return -(65535 - value) - 1
			#return value - 65536
		else:
			return value

	def get_gyro(self):
		gyro_x = self.__read_address(MPU6050.GYRO_X)
		gyro_y = self.__read_address(MPU6050.GYRO_Y)
		gyro_z = self.__read_address(MPU6050.GYRO_Z)

		gx = gyro_x/MPU6050.GYRO_SCALE[gyro_mode]
		gy = gyro_y/MPU6050.GYRO_SCALE[gyro_mode]
		gz = gyro_z/MPU6050.GYRO_SCALE[gyro_mode]

		return np.array([gx, gy, gz])

	def get_acc(self):
		acc_x = self.__read_address(MPU6050.ACC_X)
		acc_y = self.__read_address(MPU6050.ACC_Y)
		acc_z = self.__read_address(MPU6050.ACC_Z)

		ax = acc_x/MPU6050.ACC_SCALE[acc_mode]
		ay = acc_y/MPU6050.ACC_SCALE[acc_mode]
		az = acc_z/MPU6050.ACC_SCALE[acc_mode]

		return np.array([ax, ay, az])

	def calibrate(self, iterations):
		a = np.array([0.0, 0.0, 0.0])
		w = np.array([0.0, 0.0, 0.0])
		for n in range(iterations):
			a = a + self.get_acc()
			w = w + self.get_gyro()
		return [a/iterations, w/iterations]

# setup()
mpu = MPU6050()

a_off, w_off = mpu.calibrate(1000)
t = 0.0
while True:
	dt = datetime.now().microsecond - t
	t = t + dt

	a = mpu.get_acc() - a_off
	w = mpu.get_gyro() - w_off

	print('t\t', t)
	print('acc\t', a)
	print('gyro\t', w)
	print()

	with open('output.log', 'a') as f:
		f.write('\n{},{}'.format(a**dt, w*dt))
