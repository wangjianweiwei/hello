# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/11/1 9:00 下午
"""
from hello.server import server
from hello.router import Route
from hello.response import json
from hello.exception import ExceptionHandle


class Hello:

    def __init__(self):
        self.router = Route()
        self.exception_handle = ExceptionHandle(app=self)

    async def handle_request(self, request, response_callback):
        try:
            handle = self.router.get(request)

            response = await handle(request)
        except Exception as e:
            response = self.exception_handle.response(request, e)

        response_callback(response)

    def route(self, url, method):
        def response(handle):
            self.router.add(url=url, method=method, handle=handle)
            return handle

        return response

    def run(self, host, port):
        try:
            server(host=host, port=port, request_handle=self.handle_request)
        except:
            pass


if __name__ == '__main__':
    app = Hello()


    @app.route('/index', method="GET")
    async def index(request):
        return json({"name": True})


    app.run("0.0.0.0", port=8000)
