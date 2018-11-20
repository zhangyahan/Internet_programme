from socket import *

ip_port = ('127.0.0.1', 9999)
buffer_size = 1024


ntp_client = socket(AF_INET, SOCK_DGRAM)

while True:
    # 发送消息
    msg = input('>>>').strip()
    ntp_client.sendto(msg.encode('utf-8'), ip_port)

    # 返回消息
    data, client_ip_port = ntp_client.recvfrom(buffer_size)
    print('NTP服务器的标准时间是', data.decode())
