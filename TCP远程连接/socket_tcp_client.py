from socket import *
import struct
from functools import partial


ip_port = ('127.0.0.1', 9999)
back_log = 5
buffer_size = 1024

tcp_client = socket(AF_INET, SOCK_STREAM)
tcp_client.connect(ip_port)

while True:
    cmd = input('>>').strip()
    if not cmd: continue
    if cmd == 'quit': break

    tcp_client.send(cmd.encode('utf-8'))

    # 解决粘包
    length_data = tcp_client.recv(4)
    length = struct.unpack('i', length_data)[0]

    recv_msg = ''.join(iter(partial(tcp_client.recv, buffer_size), b''))

    print(recv_msg.decode('gbk'))
tcp_client.close()
