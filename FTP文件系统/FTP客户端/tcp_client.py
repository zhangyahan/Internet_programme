from socket import *

ip_port = ('127.0.0.1', 9999)
buffer_size = 1024


ftp_client = socket(AF_INET, SOCK_STREAM)
ftp_client.connect(ip_port)

while True:
    data = ftp_client.recv(buffer_size).decode('utf-8')
    msg = input('>>').strip().encode('utf-8')
    if not msg:
        break
    if msg == 'quit':
        break
    ftp_client.send(msg)
    print(data)

ftp_client.close()
