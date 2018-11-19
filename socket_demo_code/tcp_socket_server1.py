import socket

# 创建基于网络通信的TCP套接字
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定地址(ip, port,)
phone.bind(('127.0.0.1', 8888))
# 设置监听套接字(服务器端必须设置为监听套接字)
phone.listen(5)

# 等待客户端连接,accept()返回一个元祖,(client, addr,)
conn, addr = phone.accept()
# 收发消息之间使用的二进制字节
# 接收客户端发送的消息
msg = conn.recv(1024)
print('客户端发来的消息是{}'.format(msg))
# 发送消息
conn.send(msg.upper())
# 关闭客户端
conn.close()
# 关闭服务器
phone.close()


