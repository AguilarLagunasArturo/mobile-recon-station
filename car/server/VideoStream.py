from flask import Flask, render_template_string

class VideoStream:
    def __init__(frame, host, port):
        self.frame = frame
        self.host = host
        self.port = port

    def start(self):
        app = Flask('MRS')
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

        app.run(debug=False, host='192.168.1.80', port=9090)
