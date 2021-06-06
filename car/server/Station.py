import socket
import threading
class Station:

	def __init__(self, html_path, js_path, css_path, ip=socket.gethostbyname(socket.gethostname()), port=3141, video_port=6282, format='utf-8'):
		self.HOST = ip
		self.PORT = port
		self.VIDEO_PORT = video_port
		self.FORMAT = format

		# Create server to stream data through the internet
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind( (self.HOST, self.PORT) )

		self.current_state = 0
		self.running = True

		RESPONSE_BEGIN = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\n'
		with open(html_path, 'r') as f:
			html = f.read().split('\n')
			html[11] = 'src="http://{}:{}"'.format(self.HOST, self.VIDEO_PORT)
			html_begin = '\n'.join(html[0:3])
			html_end = '\n'.join(html[5:])
			print(html_end)
		with open(js_path, 'r') as f:
			js = f.read()
			js = '<script>\n{}</script>'.format(js)
		with open(css_path, 'r') as f:
			css = f.read()
			css = '<style>\n{}</style>'.format(css)
		RESPONSE_BODY = '{}\n{}\n{}\n{}'.format(html_begin, js, css, html_end)
		RESPONSE_END = '\n\r\n'
		self.RESPONSE = '{}{}{}'.format(RESPONSE_BEGIN, RESPONSE_BODY, RESPONSE_END).encode(self.FORMAT)

	@staticmethod
	def get_local_ip():
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		local_ip = s.getsockname()[0]
		s.close()
		return local_ip

	def __handle_client(self, conn, addr):
		print('[CLIENT] new connection {}'.format(addr))
		while True:
			message = conn.recv(1024).decode(self.FORMAT)
			if message:
				#print('[{}] {}'.format(addr, message))
				if len(message.split('\n')[-1]) > 0:
					self.current_state = int(message.split('\n')[-1][-1])
					print('[{}] {}'.format(addr, self.current_state))
				else:
					conn.send(self.RESPONSE)
				break
		conn.close()

	def __handle_connections(self):
		print('[STARTING] {}:{}'.format(self.HOST, self.PORT))
		self.server.listen()
		while self.running:
			conn, addr = self.server.accept() # blocking until connection accepted
			t = threading.Thread(target=self.__handle_client, args=(conn, addr))
			t.start()
			#print('[CONNECTIONS] {}'.format(threading.activeCount() -1))

	def start(self):
		main_t = threading.Thread(target=self.__handle_connections, args=())
		main_t.start()

	def stop(self):
		self.running = False
