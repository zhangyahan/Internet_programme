from socket import *

ip_port = ('127.0.0.1', 9999)
back_log = 5
buffer_size = 1024

tcp_server = socket(AF_INET, SOCK_STREAM)
tcp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcp_server.bind(ip_port)
tcp_server.listen(back_log)

while True:
    conn, address = tcp_server.accept()
    print('双向连接', conn)
    print('客户端地址', address)
    while True:
        try:
            print(address, '以连接')
            data = conn.recv(buffer_size)
            if not data:
                break
            print('客户端的消息', data.decode('utf-8'))
            conn.send(data.upper())
            print('服务器已发送消息')
        except ConnectionResetError:
            break
    conn.close()
tcp_server.close()
