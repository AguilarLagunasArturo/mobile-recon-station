import socket
import threading

PORT = 5050
SERVER = '192.168.1.80'
#SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
EXIT_CODE = 'exit'
RESPONSE_BEGIN = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\n'
with open('joystick/index.html', 'r') as f:
    html = f.read().split('\n')
    html_begin = '\n'.join(html[0:3])
    html_end = '\n'.join(html[5:])
with open('joystick/logic.js', 'r') as f:
    js = f.read()
    js = '<script>\n{}</script>'.format(js)
with open('joystick/look.css', 'r') as f:
    css = f.read()
    css = '<style>\n{}</style>'.format(css)
RESPONSE_BODY = '{}\n{}\n{}\n{}'.format(html_begin, js, css, html_end)
RESPONSE_END = '\n\r\n'
RESPONSE = '{}{}{}'.format(RESPONSE_BEGIN, RESPONSE_BODY, RESPONSE_END).encode(FORMAT)
print(RESPONSE)

# Create server to stream data through the internet
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind( (SERVER, PORT) )

def handle_client(conn, addr):
    print('[CLIENT] new connection {}'.format(addr))
    while True:
        message = conn.recv(1024).decode(FORMAT)
        if message:
            print('[{}] {}'.format(addr, message))
            conn.send(RESPONSE)
            break
            '''if message == EXIT_CODE:
                print('[CLIENT] connection ended {}'.format(addr))
                break'''
    conn.close()

def start():
    server.listen(2)
    while True:
        conn, addr = server.accept() # blocking until connection accepted
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()
        print('[CONNECTIONS] {}'.format(threading.activeCount() -1))

print('[STARTING] {} at port {}'.format(SERVER, PORT))
start()
