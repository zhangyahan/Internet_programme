import socketserver


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        print('conn is', self.request)  # conn
        print('address is', self.client_address)  # address

        while True:
            # 收消息
            data = self.request.recv(1024)
            print("收到客户端的消息是", data)

            # 发消息
            self.request.sendall(data.upper())


if __name__ == '__main__':
    s = socketserver.ThreadingUDPServer(('127.0.0.1', 9999), MyServer)  # 多线程
    # s = socketserver.ForkingTCPServer(('127.0.0.1', 9999), MyServer)  # 多进程
    s.serve_forever()
