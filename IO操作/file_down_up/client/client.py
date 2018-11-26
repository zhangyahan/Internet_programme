import socket
import os,sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class selectFtpclient(object):

    def __init__(self):
        self.args = sys.argv
        if len(self.args) > 1:
            self.port = (self.args[1], int(self.args[2]))
        else:
            self.port = ('127.0.0.1', 9999)
        self.create_socket()
        self.command_fanout()

    def create_socket(self):
        try:
            self.sock = socket.socket()
            self.sock.connect(self.port)
            print('连接服务器成功')
        except Exception as e:
            print('error', e)
        
    def command_fanout(self):
        while 1:
            cmd = input('>>>').strip()
            if cmd == 'exit()':
                break
            cmd, filename = cmd.split()
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                func(cmd, filename)
            else:
                print('调用错误')
    
    def put(self, cmd, filename):
        if os.path.isfile(filename):
            filename = os.path.basename(filename)
            filesize = os.path.getsize(filename)
            fileinfo = '{}|{}|{}'.format(cmd, filename, str(filesize))
            self.sock.send(fileinfo.encode('utf-8'))
            recvStatus = self.sock.recv(1024)
            hasSend = 0
            if recvStatus.decode('utf-8') == 'OK':
                print('文件信息已发送')
                with open(filename, 'rb') as f:
                    while hasSend < filesize:
                        data = f.read(1024)
                        self.sock.send(data)
                        hasSend += len(data)
                        s = str(int(hasSend/filesize*100)) + '%'
                        print('[{}] {}'.format(filename, s), end='\r')
                print('\n文件上传完毕')


    def get(self, cmd, filename):
        pass
    

if __name__ == "__main__":
    selectFtpclient()
