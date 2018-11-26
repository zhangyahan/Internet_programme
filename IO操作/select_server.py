import select
import socket


sock = socket.socket()
sock.bind(('127.0.0.1', 9999))
sock.listen(5)

r_list = [sock, ]

while 1:
    r, w, s, = select.select(r_list, [], [])
    
    for i in r:
        if i == sock:
            conn, addr = i.accept()
            r_list.append(conn)
        else:
            while 1:
                data = conn.recv(1024)
                if not data:
                    r_list.remove(i)
                    i.close()
                    break   
                print(data.decode('utf-8'))
                conn.send(b"hello")
    