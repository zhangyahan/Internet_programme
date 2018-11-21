import json
import os
import hashlib
import socketserver
import configparser
from conf import settings


class ServerHandler(socketserver.BaseRequestHandler):
    # 重写handle方法
    def handle(self):

        while 1:
            # conn = self.request
            data = self.request.recv(1024).strip()
            data = json.loads(data.decode('utf-8'))
            # '''
            #     {
            #         "action": "auth",
            #         "username": "username",
            #         "password": "password",
            #     }
            # '''
            print(data.get('action'))
            if data.get('action'):
                if hasattr(self, data.get('action')):
                    # 反射查找函数
                    func = getattr(self, data.get('action'))
                    func(**data)
                else:
                    print('Invalid cmd')
            else:
                print('Invalid cmd')

    def send_response(self, status_code):
        response = {'status_code': status_code}
        self.request.send(json.dumps(response).encode('utf-8'))

    def auth(self, **kwargs):
        print(kwargs)
        username = kwargs.get('username')
        password = kwargs.get('password')

        username = self.authenticate(username, password)
        if username is not None:
            self.send_response(2000)
        else:
            self.send_response(3333)

    def authenticate(self, username, password):
        # cfg = configparser.ConfigParser()
        # cfg.read(settings.ACCOUNTS_PATH)
        # if username in cfg.sections():
        #     if cfg[username]['Password'] == password:
        #         print('passed authenticate')
        if username == 'zyh' and password == '123':
            self.username = username
            # 用户主目录和用户名
            self.basedir = os.path.join(settings.BASE_DIR, 'home', self.username)
            return username

    def put(self, **kwargs):
        print(kwargs)
        file_name = kwargs.get('file_name')
        file_size = kwargs.get('file_size')
        target_path = kwargs.get('target_path')

        # 文件指定路径
        abs_path = os.path.join(self.basedir, target_path, file_name)

        ###########################################
        # 判断文件后是否存在
        has_received = 0
        if os.path.exists(abs_path):
            file_has_size = os.path.getsize(abs_path)
            if file_has_size < file_size:
                # 断点续传
                self.request.send('CHANGE'.encode('utf-8'))
                choice = self.request.recv(1024).decode('utf-8')
                if choice == "Y":
                    self.request.sendall(str(file_has_size).encode('utf-8'))
                    has_received += file_has_size
                    f = open(abs_path, 'ab')
                else:
                    f = open(abs_path, 'wb')
            else:
                # 文件完全存在
                self.request.send('NO_CHANGE'.encode('utf-8'))
                return
        else:
            self.request.send('NO_FILE'.encode('utf-8'))
            f = open(abs_path, 'wb')

        s = hashlib.md5()
        while has_received < file_size:
            try:
                data = self.request.recv(1024)
            except Exception as e:
                print(e)
                break
            f.write(data)
            has_received += len(data)
            s.update(data)
        f.close()
        shm = s.hexdigest()
        hm = self.request.recv(1024).decode('utf-8')
        print('server>>>>', shm)
        print('client>>>>', hm)
        if shm != hm:
            self.request.send('X'.encode('utf-8'))
        self.request.send('V'.encode('utf-8'))

    def ls(self, **kwargs):
        file_list = os.listdir(self.basedir)
        file_str = '\n'.join(file_list)
        if not len(file_list):
            file_str = '<no file>'
        self.request.sendall(file_str.encode('utf-8'))

    def cd(self, **kwargs):
        dirname = kwargs.get('dirname')
        if dirname == '..':
            self.basedir = os.path.dirname(self.basedir)
        else:
            if os.path.exists(dirname):
                self.basedir = os.path.join(self.basedir, dirname)
            else:
                self.request.sendall('NO'.encode('utf-8'))

        self.request.sendall(self.basedir.encode('utf-8'))

    def mkdir(self, **kwargs):
        dirname = kwargs.get('dirname')
        path = os.path.join(self.basedir, dirname)
        if not os.path.exists(path):
            if '/' in dirname:
                os.makedirs(path)
            else:
                os.mkdir(path)
            self.request.send('创建成功'.encode('utf-8'))
        else:
            self.request.send('{}文件已存在'.format(dirname).encode('utf-8'))
