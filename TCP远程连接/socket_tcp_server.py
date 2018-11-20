from socket import *
import subprocess
import struct

ip_port = ('127.0.0.1', 9999)
back_log = 5
buffer_size = 1024


tcp_server = socket(AF_INET, SOCK_STREAM)
tcp_server.bind(ip_port)
tcp_server.listen(back_log)

while True:
    conn, address = tcp_server.accept()
    print('新的客户端', address)
    while True:
        try:
            cmd = conn.recv(buffer_size)
            if not cmd:
                break
            print('客户端的命令是', cmd)
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
            # 将数字打包成四个字节
            conn.send(struct.pack('i', len(cmd_res)))
            conn.send(cmd_res)

        except Exception as e:
            print(e)
            break
    conn.close()
