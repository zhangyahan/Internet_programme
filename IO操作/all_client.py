import socket


sock = socket.socket()
sock.connect(('127.0.0.1', 1234))

while 1:
    msg = input('>>>')
    if not msg:
        sock.close()
        break
    sock.send(msg.encode('utf-8'))
    data = sock.recv(2014)
    print(data.decode('utf-8'))
