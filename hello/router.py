# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/11/2 2:26 下午
"""
from hello.exception import NotFound


class Route:

    def __init__(self):
        self.routes = {}

    def add(self, url, method, handle):
        self.routes[url] = {"method": method, "handle": handle}

    def get(self, request):
        match = self.routes.get(request.url)
        if match and match['method'] == request.method:
            return match['handle']

        raise NotFound("Requested URL {} not found".format(request.url))
