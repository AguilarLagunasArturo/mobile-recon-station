#!/usr/bin/env python3

''' Modules '''
from cv_recon.picam import PiCamStream
from cv_recon import Colorspace
from cv_recon import cv_tools
from mobile.MotorDriver import MotorDriver
from server.Station import Station
import numpy as np
import cv2 as cv

from RPi import GPIO
from time import sleep

''' Station '''
mobile_station = Station(
	'server/joystick/index.html',
	'server/joystick/logic.js',
	'server/joystick/look.css',
	'192.168.1.82', 3141
)
mobile_station.start()
''' Raspberry stuff '''
motor_pins = (11, 13, 15, 16) #r1, r2, l1, l2
# help(GPIO)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
wheels = MotorDriver(motor_pins)
# wheels.warmup()

''' Recon stuff '''
x_th = 0.5
MANUAL_MODE = 0
RECON_MODE = 1
MODE = MANUAL_MODE

''' Cam stuff '''
res = (320, 240)
fps = 32

if MODE == RECON_MODE:
	# initialize the camera
	cam_stream = PiCamStream(res, fps)
	cam_stream.start()

	# color recon obj
	colorspace = Colorspace('last.log')
	#colorspace.createSliders()

	# warmup camera
	sleep(2.0)

while True:
	if MODE == RECON_MODE:
		''' RECON_MODE '''
		#colorspace.updateHSV()
		frame = cam_stream.current_frame
		frame_blur = cv.GaussianBlur(frame, (9, 9), 150)                # smoothes the noise
		frame_hsv = cv.cvtColor(frame_blur, cv.COLOR_BGR2HSV)           # convert BGR to HSV

		boxes = colorspace.getMaskBoxes(frame, frame_hsv, 150)  # get boxes (x, y, w, h)

		offsets = cv_tools.getBoxesOffset(frame, boxes)                 # get boxes offset from the center of the frame
		if len(offsets) == 1:
			if offsets[0][0] < -x_th:
				wheels.move(MotorDriver.RIGHT)
			elif offsets[0][0] > x_th:
				wheels.move(MotorDriver.LEFT)
			else:
				wheels.move(MotorDriver.STOP)
		else:
			wheels.move(MotorDriver.STOP)
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
	elif MODE == MANUAL_MODE:
		''' MANUAL_MODE '''
		wheels.move(mobile_station.current_state)
		# TODO:
		# - CONTROL DIR FROM WIFI OR BT

wheels.move(MotorDriver.STOP)
mobile_station.stop()
cam_stream.close()
cv.destroyAllWindows()
#colorspace.dumpSettings()
