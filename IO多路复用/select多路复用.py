import socket
import select



def client(conn):
    data = conn.recv(1024)
    print(data.decode('utf-8'))
    conn.sned(data)


def main(ip_port, buffer_size, back):
    sock = socket.socket()
    sock.bind(ip_port)
    sock.listen(back)

    r_list = [sock, ]
    w_list = []
    e_list = []

    sel = select.select(r_list, w_list, e_list)

    for i in sel:
        if i == sock:
            conn, addr = i.accept()
            print(addr)
            r_list.appent(conn)
        else:
            client(i)


if __name__ == '__main__':
    ip_port = ('127.0.0.1', 9999)
    buffer_size = 1024
    back = 5
    main(ip_port, buffer_size, back)
    



