''' Modules '''
from RPi import GPIO
from time import sleep

''' Raspberry stuff '''
motor_pins = [11, 13, 15, 16] #r1, r2, l1, l2

# help(GPIO)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
for mp in motor_pins:
	GPIO.setup(mp, GPIO.OUT)
	GPIO.output(mp, GPIO.LOW)


current_state = 0	# 0, 1, 2, 3, 4
'''states = [
	[0, 0, 0, 0],	# 0: stop
	[1, 0, 1, 0],	# 1: forward
	[0, 1, 0, 1],	# 2: backward
	[0, 1, 1, 0],	# 3: right
	[1, 0, 0, 1]	# 4: left
]'''
states = [
	[0, 0, 0, 0],	# 0: stop
	[1, 0, 0, 1],	# 1: forward
	[0, 1, 1, 0],	# 2: backward
	[0, 1, 0, 1],	# 3: right
	[1, 0, 1, 0]	# 4: left
]

def set_state(new_state):
	global current_state
	if current_state != new_state:
		current_state = new_state
		if current_state == 0:
			print('stop')
		elif current_state == 1:
			print('forward')
		elif current_state == 2:
			print('backward')
		elif current_state == 3:
			print('right')
		else:
			print('left')
		for mp,s in zip(motor_pins, states[new_state]):
			GPIO.output(mp, s)

set_state(1)
sleep(3)
set_state(2)
sleep(3)
set_state(3)
sleep(3)
set_state(4)
sleep(3)
set_state(0)
sleep(3)
