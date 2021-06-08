import smbus

''' CONSTANTS '''
ACC_SCALE_2G = 16384.0
GYRO_SCALE_250D = 250.0

''' REGISTERS [links] '''
ADD = 0x68

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
	pass

def read(add):
	pass

def get_acc():
	pass

def get_gyro():
	pass


