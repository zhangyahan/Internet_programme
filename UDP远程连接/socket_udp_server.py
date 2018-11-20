from socket import *
import subprocess

ip_port = ('127.0.0.1', 9999)
back_log = 5
buffer_size = 1024


udp_server = socket(AF_INET, SOCK_DGRAM)
udp_server.bind(ip_port)


while True:
        cmd, address = udp_server.recvfrom(buffer_size)
        print(address)
        print('客户端的命令是', cmd.decode('utf-8'))
        # 执行命令, 得到命令的结果cmd_res
        res = subprocess.Popen(cmd.decode('utf-8'),
                               shell=True,
                               stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE)

        err = res.stderr.read()
        if err:
            cmd_res = err
        else:
            cmd_res = res.stdout.read()
        # 发
        if not cmd_res:
            cmd_res = '执行成功'.encode('gbk')
        udp_server.sendto(cmd_res, address)

