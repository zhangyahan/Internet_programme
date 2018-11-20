from socket import *
import os
import sys
import hmac


secret_key = b"zyh bang bang bang"

def conn_auth(conn):
    """
    判断链接是否合法
    return Ture or False
    """
    print('开始验证新链接的合法性')
    msg = os.urandom(32)
    conn.send(msg)
    h = hmac.new(secret_key, msg)
    digest = h.digest()
    respone = conn.recv(len(digest))
    return hmac.compare_digest(respone, digest)


def data_handler(conn, address, bufsize=1024):
    """
    只处理消息的收发
    """
    if not conn_auth(conn):
        print('链接不合法,关闭')
        conn.close()
        return
    print('链接合法,开始通信')
    while True:
        data = conn.recv(bufsize)
        if not data:
            print('客户端[{0}:{1}]断开连接'.format(address[0], address[1]))
            break
        print(data.decode('utf-8'))
        conn.send(data)

def server_handler(ip_port, bufsize, backlog=5):
    """
    只处理链接
    :param ip_port:
    :return
    """
    tcp_socket_server = socket(AF_INET, SOCK_STREAM)
    tcp_socket_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcp_socket_server.bind(ip_port)
    tcp_socket_server.listen(backlog)
    
    while True:
        try:
            conn, address = tcp_socket_server.accept()
        except KeyboardInterrupt as e:
            sys.exit('服务器以关闭')
        print('新连接[{0}:{1}]'.format(address[0], address[1]))
        data_handler(conn, address, bufsize)


if __name__ == '__main__':
    ip_port = ('127.0.0.1', 9999)
    bufsize = 1024
    server_handler(ip_port, bufsize)


