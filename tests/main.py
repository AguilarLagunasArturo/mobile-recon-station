''' Modules '''
from cv_recon.picam import PiCamStream
from cv_recon import Colorspace
from cv_recon import cv_tools
import numpy as np
import cv2 as cv

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

'''
states = [
	[0, 0, 0, 0],	# 0: stop
	[1, 0, 1, 0],	# 1: forward
	[0, 1, 0, 1],	# 2: backward
	[0, 1, 1, 0],	# 3: right
	[1, 0, 0, 1]	# 4: left
]
'''

states = [
	[0, 0, 0, 0],	# 0: stop
	[1, 0, 0, 1],	# 1: forward
	[0, 1, 1, 0],	# 2: backward
	[0, 1, 0, 1],	# 3: right
	[1, 0, 1, 0]	# 4: left
]

def set_state(state):
	if state == 'f':
		new_state = 1
	elif state == 'b':
		new_state = 2
	elif state == 'r':
		new_state = 3
	elif state == 'l':
		new_state = 4
	else:
		new_state = 0
	global current_state
	if current_state != new_state:
		#print(state)
		current_state = new_state
		for mp,s in zip(motor_pins, states[new_state]):
			GPIO.output(mp, s)

''' Recon stuff '''
x_th = 0.5

''' Cam stuff '''
res = (320, 240)
fps = 32

# initialize the camera
cam_stream = PiCamStream(res, fps)
cam_stream.start()

# color recon obj
colorspace = Colorspace('last.log')
#colorspace.createSliders()

# warmup camera
sleep(2.0)

# capture frames from the camera
while True:
	''' RECON_MODE '''
	#colorspace.updateHSV()
	frame = cam_stream.current_frame
	frame_blur = cv.GaussianBlur(frame, (9, 9), 150)                # smoothes the noise
	frame_hsv = cv.cvtColor(frame_blur, cv.COLOR_BGR2HSV)           # convert BGR to HSV

	boxes = colorspace.getMaskBoxes(frame, frame_hsv, 150)  # get boxes (x, y, w, h)

	offsets = cv_tools.getBoxesOffset(frame, boxes)                 # get boxes offset from the center of the frame
	if len(offsets) == 1:
		if offsets[0][0] < -x_th:
			set_state('r')
		elif offsets[0][0] > x_th:
			set_state('l')
		else:
			set_state('s')
	else:
		set_state('s')
	# Print data
	#for i, offset in enumerate(offsets):
	#       print(i, offset)                                    # print offset (x_off, y_off)

	frame_out = cv_tools.drawBoxes(frame.copy(), boxes)     # draw boxe
	frame_out = cv_tools.drawBoxesPos(frame_out, boxes)     # draw offsets

	frame_grid = cv_tools.grid(frame, (2, 3),[              # generate grid
		frame_hsv, frame_out, colorspace.im_contours,
		colorspace.im_cut, colorspace.im_mask, colorspace.im_edges], 0.8)

	cv.imshow('grid', frame_grid)                           # show grid

	if cv.waitKey(1) & 0xFF == ord("q"):
		break

	''' MANUAL_MODE '''
	# TODO:
	# - CONTROL DIR FROM WIFI OR BT

set_state('s')
cam_stream.close()
cv.destroyAllWindows()
#colorspace.dumpSettings()
