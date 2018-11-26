import selectors
import socket

sel = selectors.DefaultSelector()  # 创建一个最合适的IO多路复用方式


def accept(sock, mask):
    conn, addr = sock.accept()
    print(conn, addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    try:
        data = conn.recv(1024)
        if not data:
            raise Exception
        print(data.decode('utf-8'))
        conn.send(b'OK')
    except Exception as e:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()


sock = socket.socket()
sock.bind(('127.0.0.1', 1234))
sock.listen(100)
sock.setblocking(False)

sel.register(sock, selectors.EVENT_READ, accept)  # 进行注册

while 1:
    events = sel.select()
    for key, mask in events:
        print(key)
        print(mask)
        callback = key.data  # 获取绑定的函数
        callback(key.fileobj, mask)  # 将key的对象传入函数
