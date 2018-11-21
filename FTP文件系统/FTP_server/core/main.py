# 主逻辑函数
import optparse  # 解析命令行的命令
import socketserver
from conf import settings
from core import server


class ArgvHandler(object):

    def __init__(self):
        self.op = optparse.OptionParser()
        # self.op.add_option('-s', '--server', dest='server')
        # self.op.add_option('-P', '--port', dest='port')
        options, args = self.op.parse_args()
        self.verify_args(options, args)

    def verify_args(self, options, args):
        """
        验证命令行选项参数
        """
        cmd = args[0]
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            func()
    
    def start(self):
        print('the server is working')
        sock_server = socketserver.ThreadingTCPServer((settings.IP,
                                                       settings.PORT),
                                                       server.ServerHandler)
        sock_server.serve_forever()
    
    def help(self):
        pass
