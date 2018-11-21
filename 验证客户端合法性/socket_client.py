import os
import sys
import hmac
from socket import *

secret_key = b'zyh bang bang bang'


def conn_auth(conn):
    """
    验证客户端到服务器的连接
    :param conn:
    :return:
    """
    msg = conn.recv(32)
    h = hmac.new(secret_key, msg)
    digest = h.digest()
    conn.sendall(digest)


def client_handler(ip_port, bufsize=1024):
    """
    连接客户端并进行收发
    """
    tcp_client = socket(AF_INET, SOCK_STREAM)
    tcp_client.connect(ip_port)
    
    # 验证
    conn_auth(tcp_client)

    while True:
        msg = input('>>>').strip()
        if not msg:
            continue
        if msg == 'exit':
            sys.exit('bye')
        tcp_client.send(msg.encode('utf-8'))
        data = tcp_client.recv(bufsize)
        print(data.decode('utf-8'))
            

if __name__ == '__main__':
    ip_port = ('127.0.0.1', 9999)
    client_handler(ip_port)
