import socket
import threading

PORT = 5050
SERVER = '127.0.1.1'
FORMAT = 'utf-8'
EXIT_CODE = 'exit'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect( (SERVER, PORT) )

def send(msg):
    client.send(msg.encode(FORMAT))

while True:
    msg = input('Send: ')
    send(msg)
    if msg == 'exit':
        break
