import socket


sock = socket.socket()
sock.connect(('127.0.0.1', 9999))

sock.send(b'hello')
data = sock.recv(1024)
print(data)
sock.close()

