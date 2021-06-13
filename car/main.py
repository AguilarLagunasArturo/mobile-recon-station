#!/usr/bin/env python3

''' Modules '''
from cv_recon.picam import PiCam
from cv_recon import Colorspace
from cv_recon import cv_tools

from mobile.MotorDriver import MotorDriver
from mobile.MPU6050 import MPU6050

from server.Station import Station
from flask import Flask, render_template_string, Response
import numpy as np
import cv2 as cv
import threading

from RPi import GPIO
from time import sleep
from time import time

''' Cnt '''
HOST = Station.get_local_ip()
VIDEO_PORT = 6282
JOYSTICK_PORT = 3141

''' Station '''
mobile_station = Station(
	'server/joystick/index.html',
	'server/joystick/logic.js',
	'server/joystick/look.css',
	HOST, JOYSTICK_PORT, VIDEO_PORT
)
mobile_station.start()

''' Video Streaming '''
frame = []
update = False
app = Flask(__name__)

@app.route('/')
def index():
	return render_template_string('''<html>
	<head>
		<title>Stream</title>
	</head>
	<body>
		<img src="{{ url_for('stream') }}" width="100%">
	</body>
 	</html>''')

@app.route('/stream')
def stream():
	return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_frames():
	global frame
	global update
	while True:
		if update:
			sleep(0.1)
			ret, buffer = cv.imencode('.jpg', frame)
			frame = buffer.tobytes()
			yield (b'--frame\r\n'
				 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def start_flask():
	app.run(debug=False, host=HOST, port=VIDEO_PORT)

t_flask = threading.Thread(target=start_flask, args=())
t_flask.start()

''' MPU6050 '''
def readMPU():
	mpu = MPU6050()

	a_off, w_off = mpu.calibrate(500)
	t_off = time()
	t = 0
	dt = 0
	print('[MPU] Started')
	while True:
		dt = time() - (t_off + t)
		t = t + dt

		a = mpu.get_acc() - a_off
		w = mpu.get_gyro() - w_off

		ax, ay, az = a
		wx, wy, wz = w

		with open('output.log', 'a') as f:
			f.write('\n{},{},{},{},{},{},{},{}'.format(t, dt, ax, ay, az, wx, wy, wz))

t_mpu = threading.Thread(target=readMPU, args=())
t_mpu.start()

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
#MODE = RECON_MODE

''' Cam stuff '''
res = (320, 240)
fps = 24

if MODE == RECON_MODE:
	# color recon obj
	colorspace = Colorspace('last.log')
	#colorspace.createSliders()

# initialize the camera
cam = PiCam(res, fps, contrast=10, brightness=55)
cam.videoCapture()
# warmup camera
sleep(2.0)

while True:
	frame = cam.current_frame
	if MODE == RECON_MODE:
		''' RECON_MODE '''
		#colorspace.updateHSV()
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
		cs = mobile_station.current_state
		if cs >= 0 and cs <= 4:
			wheels.move(cs)
		# TODO:
		# - CONTROL DIR FROM WIFI OR BT
	update = True

wheels.move(MotorDriver.STOP)
mobile_station.stop()
cam.release()
cv.destroyAllWindows()
#colorspace.dumpSettings()
