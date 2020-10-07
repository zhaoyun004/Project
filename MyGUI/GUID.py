#!/usr/bin/python3

import socket
import sys

# 创建 socket 对象
serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM) 

# 获取本地主机名
host = socket.gethostname()
print(host)

port = 9999

# 最好是bind 0.0.0.0,这样127.0.0.1, localhost，以及192.168... 客户都可以连接:
serversocket.bind(('0.0.0.0', port))

# bind公网地址会失败？p2p软件怎么做的？
# serversocket.bind(('36.7.226.209', port))


# 设置最大连接数，超过后排队
serversocket.listen()

while True:
    # accept函数返回一个元组(a ,b)，将a赋给clientsocket, b赋给addr。
    clientsocket,addr = serversocket.accept()      
    
    print("Address: %s" % str(addr))
    
    data = clientsocket.recv(1024)
    print(data)
    
    msg = 'Welcome to Server\n'
    clientsocket.send(msg.encode('utf-8'))
    
    clientsocket.close()
