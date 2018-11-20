import struct
import pickle
from socket import *
from functools import partial


class FtpServer(object):

    def __init__(self, ip, port, back_log, buffer_size=1024):
        self.buffer_size = buffer_size
        self.ftp_server = socket(AF_INET, SOCK_STREAM)
        self.ftp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.ftp_server.bind((port, ip))
        self.ftp_server.listen(back_log)

    def start(self):
        print('已启动程序.....')
        menu = self.user_menu()
        while True:
            conn, address = self.ftp_server.accept()
            print('客户端连接', address)

            while True:
                data = conn.recv(self.buffer_size)
                if not data:
                    break
                print(data.decode('utf-8'))
                conn.send(data)
            conn.close()

    def user_menu(self):
        menu = '''
                  1.上传文件
                  2.下载文件
                  '''
        return menu

def main():
    server = FtpServer(ip=9999, port='127.0.0.1', back_log=5)
    while True:
        server.start()


if __name__ == '__main__':
    main()
