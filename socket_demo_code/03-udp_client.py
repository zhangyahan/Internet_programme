from socket import *


ip_port = ('127.0.0.1', 9999)
buffer_size = 1024

# 创建套接字, 数据报
udp_client = socket(AF_INET, SOCK_DGRAM)


while True:
    msg = input('>>>')
    udp_client.sendto(msg.encode('utf-8'), ip_port)
    data, server_ip_port = udp_client.recvfrom(buffer_size)
    print(data.decode('utf-8'))
