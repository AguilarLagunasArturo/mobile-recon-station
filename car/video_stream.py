import threading
import cv2 as cv
import numpy as np
from time import sleep
from cv_recon.cv_tools import grid
#from cv_recon.picam import PiCamStream
from server.Station import Station
from flask import Flask, render_template_string, Response

''' Joystick Server '''

html = 'server/joystick/index.html'
js = 'server/joystick/logic.js'
css = 'server/joystick/look.css'

''' Video from OpenCV '''
frame = []
update = False

''' Cam stuff '''
res = (320, 240)
fps = 32

sleep(2.0)

def using_camera():
	cam_stream = PiCamStream(res, fps)
	cam_stream.start()
	global frame
	global update
	while True:
		update = False
		frame = cam_stream.current_frame
		update = True

def using_camera_old():
	cap = cv.VideoCapture(0)
	global frame
	global update
	while True:
		update = False
		ret, frame = cap.read()	# current frame
		if ret:
			gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
			#frame = grid(frame, (1, 2), [frame, gray_frame], 0.65)
			#cv.imshow('cam', frame)
			update = True
			if cv.waitKey(1) & 0xFF == ord('q'):
				cap.release()
				break

''' Flask Server '''
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
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_frames():
	camera = cv.VideoCapture(0)
	while True:
		success, frame = camera.read()  # read the camera frame
		if not success:
			break
		else:
			ret, buffer = cv.imencode('.jpg', frame)
			frame = buffer.tobytes()
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

if __name__ == "__main__":
	#t = threading.Thread(target=using_camera, args=())
	#t.start()
	stat1 = Station(html, js, css, Station.get_local_ip(), 3141)
	stat1.start()
	#app.run(debug=False, host='192.168.1.82', port=9090)

#stat2 = Station(html, js, css, '192.168.1.80', 4050)
#stat2.start()
