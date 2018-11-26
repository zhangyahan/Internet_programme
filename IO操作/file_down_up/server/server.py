import os
import time
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import socket
import selectors


class SelectFtpServer(object):

    def __init__(self):
        self.dic = {}
        self.hasReceived = 0
        self.sel = selectors.DefaultSelector()
        self.create_socket()
        self.handler()
    
    def create_socket(self):
        sock = socket.socket()
        sock.bind(('127.0.0.1', 9999))
        sock.listen(5)
        sock.setblocking(False)
        self.sel.register(sock, selectors.EVENT_READ, self.accept)
        print('服务器已开启, 等待用户连接')
    
    def handler(self):
        while 1:
            events = self.sel.select()
            for key, mask in events:
                collback = key.data
                collback(key.fileobj, mask)

    def accept(self, conn, mask):
        conn, addr = conn.accept()
        print('客户端{}:{}以连接'.format(addr[0], addr[1]))
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)
        self.dic[conn] = {}
    
    def read(self, conn, mask):
        if not self.dic[conn]:
            data = conn.recv(1024)
            cmd, fileanme, filesize = data.decode('utf-8').split('|')
            self.dic = {conn: {'cmd': cmd, 'filename': fileanme, 'filesize': int(filesize)}}

            if cmd == 'put':
                conn.send('OK'.encode('utf-8'))
            if cmd == 'get':
                pass
        else:
            if hasattr(self, self.dic[conn]['cmd']):
                func = getattr(self, self.dic[conn]['cmd'])
                func(conn)

    def put(self, conn):
        print(conn)
        filename = self.dic[conn]['filename']
        filesize = self.dic[conn]['filesize']
        path = os.path.join(BASE_DIR, 'upload', filename)
        data_recv = conn.recv(1024)
        print(data_recv)
        self.hasReceived += len(data_recv)

        with open(path, 'ab') as f:
            f.write(data_recv)
        if self.hasReceived == filesize:
            if conn in self.dic.keys():
                self.dic[conn] = {}
        print(filename, '上传完毕')
            

    def get(self):
        pass

if __name__ == "__main__":
    SelectFtpServer()