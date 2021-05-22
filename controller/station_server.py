import socket
import threading

PORT = 5050
SERVER = '192.168.1.80'
#SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
EXIT_CODE = 'exit'

#with open('../../../controller/joystick/index.html', 'r') as f:
#    index = f.read()

RESPONSE = b"""HTTP/1.1 200 OK\r
Content-Type: text/html\r

<head>
<meta charset="utf-8">
<script>
    function send(msg){
      var url = 'localhost/#state';
      var xhr = new XMLHttpRequest();
      xhr.open('POST', url, true);
      xhr.setRequestHeader("Content-Type", "application/mobile-recon-station; charset=UTF-8");
      xhr.send('param1='+msg);
      console.log(msg);
    }
</script>
<style>
  .center{
    margin:0px auto;
    display: table;
  }
  @media screen and (max-width: 1000px) {
    .mobile-controller{ display: block; }
    .desktop-controller{ display: none; }
    .button-long{
      padding: 128px 400px;
      border-radius: 128px;
    }
    .button-normal{
      padding: 164px 200px;
      border-radius: 128px;
    }
  }
  @media screen and (min-width: 1000px) {
    .mobile-controller{ display: none; }
    .desktop-controller{ display: block; position: relative;}
    .button-long{
      padding: 64px 128px;
      border-radius: 60px;
    }
    .button-normal{
      padding: 64px;
      border-radius: 60px;
    }
  }
</style>
<title>Mobile station controller</title>
</head>

<body>

<div class="center">
  <iframe
    width="800" height="400"
    src="https://www.youtube.com/embed/sxbg4GNyN58"
    title="YouTube video player"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
  </iframe>
</div>

<div class="center">
  <div class="desktop-controller center">
    <button
        type="button"
        class="button-long"
        name="m-f"
        onmousedown="send('1');"
        onmouseup="send('0');">
    </button><br>
    <button
        type="button"
        class="button-normal"
        name="m-b"
        onmousedown="send('2');"
        onmouseup="send('0');">
    </button>
    <button
        type="button"
        class="button-normal"
        name="m-r"
        onmousedown="send('3');"
        onmouseup="send('0');">
    </button><br>
    <button
        type="button"
        class="button-long"
        name="m-l"
        onmousedown="send('4');"
        onmouseup="send('0');">
    </button>
  </div>

  <div class="mobile-controller center">
    <button
        type="button"
        class="button-long"
        name="d-f"
        ontouchstart="send('1');"
        ontouchend="send('0');">
    </button><br>
    <button
        type="button"
        class="button-normal"
        name="d-b"
        ontouchstart="send('2');"
        ontouchend="send('0');">
    </button>
    <button
        type="button"
        class="button-normal"
        name="d-r"
        ontouchstart="send('3');"
        ontouchend="send('0');">
    </button><br>
    <button
        type="button"
        class="button-long"
        name="d-l"
        ontouchstart="send('4');"
        ontouchend="send('0');">
    </button>
  </div>
</div>

</body>
</html>\n\r\n"""

# Server to stream data through the internet
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
