import socket
import threading

PORT = 5050
#SERVER = 'localhost'
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
EXIT_CODE = 'exit'
RESPONSE = b"""HTTP/1.1 200 OK\r
Content-Type: text/html\r

<html>
<form action="/test" method="post">
  <label for="fname">First name:</label>
  <input type="text" id="fname" name="fname"><br><br>
  <label for="lname">Last name:</label>
  <input type="text" id="lname" name="lname"><br><br>
  <input type="submit" value="Submit">
</form>
<button onclick="window.location.href='/algo';">Click Here</button><br><br>
</html>\n\r\n"""
# Server to stream data through the internet
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    server.listen()
    while True:
        conn, addr = server.accept() # blocking until connection accepted
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()
        print('[CONNECTIONS] {}'.format(threading.activeCount() -1))

print('[STARTING] {} at port {}'.format(SERVER, PORT))
start()
