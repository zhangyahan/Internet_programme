lst = ['a', 'b', 'd', 'e', 'c']


def test():
    return lst.pop()


l = iter(test, 'b')
for i in l:
    print(i)

from functools import partial


def add(x, y):
    return x + y


func = partial(add, 1)  # 偏函数,用来固定函数的第一个参数
print(func(3))


# recv_size = 0
# recv_msg = b''
# while recv_size < length:
#     recv_msg += tcp_client.recv(buffer_size)
#     recv_size = len(recv_msg)
# print(recv_msg.decode('gbk'))

''.join(iter(partial(tcp_cilent.recv, 1024), b''))




