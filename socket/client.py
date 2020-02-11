# -*- encoding:utf-8 -*-

import socket


def client():

    s = socket.socket()
    host = '127.0.0.1'
    port = 6666
    s.connect((host, port))

    s.send(b'hello world')

    msg = s.recv(1024)
    print('From server: %s' % msg)


if __name__ == '__main__':
    client()