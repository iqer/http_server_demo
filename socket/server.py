# -*- encoding:utf-8 -*-

import socket


def server():

    s = socket.socket()
    host = '127.0.0.1'
    port = 6666

    s.bind((host, port))
    s.listen(10)

    while True:
        c, addr = s.accept()
        print('connect from: ', addr)
        msg = c.recv(1024)
        print('From client: %s' % msg)
        c.send(msg)


if __name__ == '__main__':
    server()
