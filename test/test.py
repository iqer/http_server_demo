# -*- encoding:utf-8 -*-

import threading
import socket
import time

from server.socket_server import TCPServer
from handler.base_handler import StreamRequestHandler


class TestBaseRequestHandler(StreamRequestHandler):

    def handle(self):
        msg = self.readline()
        print('Server recv msg:' + msg)
        time.sleep(1)
        self.write_content(msg)
        self.send()
        pass


class SocketServerTest:

    def run_server(self):
        tcp_server = TCPServer(('127.0.0.1', 8889), TestBaseRequestHandler)
        tcp_server.server_forever()

    def client_connect(self):
        client = socket.socket()
        client.connect(('127.0.0.1', 8889))
        client.send(b'Hello TCPServer\r\n')
        msg = client.recv(1024)
        print('Client recv msg:' + msg.decode())

    def generate_clients(self, num):
        clients = list()
        for i in range(num):
            client_thread = threading.Thread(target=self.client_connect)
            clients.append(client_thread)
        return clients

    def run(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

        clients = self.generate_clients(10)
        for client in clients:
            client.start()

        server_thread.join()

        for client in clients:
            client.join()


if __name__ == '__main__':
    SocketServerTest().run()
