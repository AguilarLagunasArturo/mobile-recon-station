''' Modules '''
from RPi import GPIO
from time import sleep

class MotorDriver:

	STOP = 0
	FORWARD = 1
	BACKWARD = 2
	RIGHT = 3
	LEFT = 4

	STATES = (
		(0, 0, 0, 0),	# 0: stop
		(1, 0, 1, 0),	# 1: forward
		(0, 1, 0, 1),	# 2: backward
		(0, 1, 1, 0),	# 3: right
		(1, 0, 0, 1)	# 4: left
	)

	def __init__(self, motor_pins):
		self.motor_pins = motor_pins
		GPIO.setmode(GPIO.BOARD)
		for mp in self.motor_pins:
			GPIO.setup(mp, GPIO.OUT)
			GPIO.output(mp, GPIO.LOW)
		self.current_state = MotorDriver.STOP

	def move(self, new_state):
		if self.current_state != new_state:
			self.current_state = new_state
			if self.current_state == MotorDriver.STOP:
				print('stop')
			elif self.current_state == MotorDriver.FORWARD:
				print('forward')
			elif self.current_state == MotorDriver.BACKWARD:
				print('backward')
			elif self.current_state == MotorDriver.RIGHT:
				print('right')
			elif self.current_state == MotorDriver.LEFT:
				print('left')
			else:
				print('DEBUG RAISE EXCEPTION')
			for mp,s in zip(self.motor_pins, MotorDriver.STATES[new_state]):
				GPIO.output(mp, s)
	def warmup(self, sleep_time=1):
		sleep(sleep_time)
		self.move(MotorDriver.STOP)
		sleep(sleep_time)
		self.move(MotorDriver.FORWARD)
		sleep(sleep_time)
		self.move(MotorDriver.BACKWARD)
		sleep(sleep_time)
		self.move(MotorDriver.RIGHT)
		sleep(sleep_time)
		self.move(MotorDriver.LEFT)
		sleep(sleep_time)
		self.move(MotorDriver.STOP)
