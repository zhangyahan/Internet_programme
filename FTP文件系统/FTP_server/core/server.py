import socketserver


class ServerHandler(socketserver.BaseRequestHandler):
    # 重写handle方法
    def handle(self):
        print('ok')
