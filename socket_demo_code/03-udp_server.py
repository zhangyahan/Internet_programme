from socket import *


ip_port = ('127.0.0.1', 9999)
buffer_size = 1024

# 创建套接字
udp_server = socket(AF_INET, SOCK_DGRAM)  # 数据报
# 绑定地址
udp_server.bind(ip_port)

while True:
    data, client_ip_port = udp_server.recvfrom(buffer_size)
    print(data.decode('utf-8'))
    udp_server.sendto(data, client_ip_port)
