import json
import optparse
import socket
import sys
import os
import hashlib


class ClientHandler(object):

    def __init__(self):
        self.op = optparse.OptionParser()
        self.op.add_option('-s', '--server', dest='server')
        self.op.add_option('-P', '--port', dest='port')
        self.op.add_option('-u', '--username', dest='username')
        self.op.add_option('-p', '--password', dest='password')
        self.options, self.args = self.op.parse_args()
        self.verify_args()
        self.make_connection()
        self.basedir = os.path.dirname(os.path.abspath(__file__))
        self.last = 0

    def verify_args(self):
        port = self.options.port
        if 0 < int(port) < 65535:
            return True
        else:
            sys.exit('the port is in 0~65535')

    def make_connection(self):
        self.sock = socket.socket()
        self.sock.connect((self.options.server,
                           int(self.options.port)))

    def interactive(self):
        if self.authenticate():
            while True:
                file_info = input('[{}]:'.format(self.current_dir))  # put filename master
                if file_info == 'exit':
                    sys.exit('bye')
                elif file_info == '':
                    continue
                file_list = file_info.split(' ')
                # if len(file_list) < 3:
                #     print('not action')
                #     continue
                if hasattr(self, file_list[0]):
                    func = getattr(self, file_list[0])
                    func(*file_list)

    def authenticate(self):
        if self.options.username is None or self.options.password is None:
            username = input('username: ')
            password = input('password: ')
            return self.get_auth_result(username, password)
        return self.get_auth_result(self.options.username, self.options.password)

    def get_auth_result(self, username, password):
        data = {
            'action': 'auth',
            'username': username,
            'password': password,
        }
        self.sock.send((json.dumps(data)).encode('utf-8'))
        data = self.response()
        print('response:', data['status_code'])
        if data['status_code'] == 2000:
            self.username = username
            self.current_dir = self.username
            return True
        else:
            print('登陆失败')

    def response(self):
        data = json.loads(self.sock.recv(1024).decode('utf-8'))
        return data

    def put(self, *file_list):
        active, file_path, target_path = file_list
        local_path = os.path.join(self.basedir, file_path)

        file_name = os.path.basename(local_path)
        file_size = os.path.getsize(file_name)

        data = {
            'action': 'put',
            'file_name': file_name,
            'file_size': file_size,
            'target_path': target_path,
        }
        self.sock.send(json.dumps(data).encode('utf-8'))

        # 得到响应，文件是否存在
        is_exist = self.sock.recv(1024).decode('utf-8')
        # ###########################################
        has_sent = 0
        if is_exist == 'NO_FILE':
            # 无文件
            pass
        elif is_exist == 'NO_CHANGE':
            # 文件完整
            print('file in {}'.format(target_path))
            return
        elif is_exist == 'CHANGE':
            # 文件不完整
            choice = input('the file exist, but not enough, is continue?[Y/N]').strip()
            if choice.upper() == "Y":
                self.sock.send('Y'.encode('utf-8'))
                continue_position = self.sock.recv(1024).decode('utf-8')
                has_sent += int(continue_position)
            else:
                self.sock.send('N'.encode('utf-8'))

        f = open(local_path, 'rb')
        f.seek(has_sent)
        s = hashlib.md5()
        while has_sent < file_size:
            data = f.read(1024)
            self.sock.send(data)
            has_sent += len(data)
            s.update(data)
            self.show_progress(has_sent, file_size)
        f.close()
        has_md5 = s.hexdigest()
        self.sock.send(has_md5.encode('utf-8'))
        data = self.sock.recv(1024).decode('utf-8')
        if data == 'V':
            print('文件上传成功')
        elif data == 'X':
            print('本地文件与服务器文件不一致')
        print(data)
        print(has_md5)

    def show_progress(self, begin, end):
        rate = float(begin)/float(end)
        rate_num = int(rate*100)
        if self.last != rate_num:
            sys.stdout.write('\r{}% {}'.format(rate_num, '#'*rate_num))
        self.last = rate_num

    def ls(self, *args):
        data = {
            'action': 'ls'
        }
        self.sock.send(json.dumps(data).encode('utf-8'))
        file_list = self.sock.recv(1024).decode('utf-8')
        print(file_list)

    def cd(self, *args):
        data = {
            'action': 'cd',
            'dirname': args[1]
        }
        self.sock.send(json.dumps(data).encode('utf-8'))

        data = self.sock.recv(1024).decode('utf-8')
        if data == 'NO':
            print('没有该目录')
        else:
            self.current_dir = os.path.basename(data)

    def mkdir(self, *args):
        data = {
            'action': 'mkdir',
            'dirname': args[1]
        }
        self.sock.send(json.dumps(data).encode('utf-8'))
        data = self.sock.recv(1024).decode('utf-8')
        print(data)


ch = ClientHandler()
ch.interactive()
