from socket import *
import time

ip_port = ('127.0.0.1', 9999)
buffer_size = 1024


ntp_server = socket(AF_INET, SOCK_DGRAM)
ntp_server.bind(ip_port)

while True:
    data, client_ip_port = ntp_server.recvfrom(buffer_size)
    print(data)
    if not data:
        fmt = '%Y-%m-%d %X'
    else:
        fmt = data.decode('utf-8')
    back_time = time.strftime(fmt)
    ntp_server.sendto(back_time.encode('utf-8'), client_ip_port)
