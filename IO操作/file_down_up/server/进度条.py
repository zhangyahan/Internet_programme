import time
hasSend = 0
file_size = 1000

while hasSend < file_size:
    hasSend += 10
    print(file_size*100)
    print(hasSend)
    print(hasSend/file_size*100)
    print(int(hasSend/file_size*100))
    s = str(int(hasSend/file_size*100)) + '%'
    time.sleep(1)
    # print('file_name' + s, end='\r')
print()
print('完成')