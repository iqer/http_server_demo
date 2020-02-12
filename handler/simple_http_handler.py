# -*- encoding:utf-8 -*-

import os
import json
from urllib import parse

from handler.base_http_handler import BaseHttpRequestHandler

RESOURCES_PATH = os.path.join(os.path.abspath(os.path.dirname(__name__)), '../resources')


class SimpleHTTPRequestHandler(BaseHttpRequestHandler):

    def __init__(self, server, request, client_address):
        BaseHttpRequestHandler.__init__(self, server, request, client_address)

    def do_GET(self):
        found, resource_path = self.get_resources(self.path)
        if not found:
            self.write_error(404)
            self.send()
        else:
            with open(resource_path, 'rb') as f:
                fs = os.fstat(f.fileno())
                clength = str(fs[6])
                self.write_response(200)
                self.write_header('Content-Length', clength)
                # 避免跨域问题
                self.write_header('Access-Control-Allow-Origin', 'http://%s:%d' %
                                  (self.server.server_address[0], self.server.server_address[1]))
                self.end_headers()
                while True:
                    buf = f.read(1024)
                    self.write_content(buf)
                    if not buf:
                        break
        pass

    def get_resources(self, path):
        url_result = parse.urlparse(path)
        resource_path = str(url_result[2], encoding='utf-8')
        if resource_path.startswith('/'):
            resource_path = resource_path[1:]
        resource_path = os.path.join(RESOURCES_PATH, resource_path)
        if os.path.exists(resource_path) and os.path.isfile(resource_path):
            return True, resource_path
        return False, resource_path

    def do_POST(self):
        # 从请求取出如数据
        body = json.loads(self.body)
        print(body)
        username = body['username']
        password = body['password']
        # 数据校验
        if username == 'dongdongdong' and password == '123456':
            response = {'message': 'success', 'code': 0}
        else:
            response = {'message': 'failed', 'code': -1}
        response = json.dumps(response)
        # 组成应答报文
        self.write_response(200)
        self.write_header('Content-Length', len(response))
        # 避免跨域问题
        self.write_header('Access-Control-Allow-Origin', 'http://%s:%d' %
                          (self.server.server_address[0], self.server.server_address[1]))
        self.end_headers()
        self.write_content(response)
