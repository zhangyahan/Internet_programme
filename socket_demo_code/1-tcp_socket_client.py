import socket

# 创建套接字
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 发起请求
phone.connect(('127.0.0.1', 8888))
# 发送消息
phone.send(b'hello world')

data = phone.recv(1024)
print(data)

phone.close()
