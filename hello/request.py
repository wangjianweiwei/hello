# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/11/2 9:52 上午
"""
import json
from urllib.parse import parse_qs

from httptools import parse_url


class RequestParameters(dict):

    def get(self, key, default=None):
        value = super(RequestParameters, self).get(key)
        return value[0] if value else default

    def getlist(self, key, default):
        return super(RequestParameters, self).get(key, default)


class Request:

    def __init__(self, url_bytes, headers, version, method):
        url_parsed = parse_url(url_bytes)
        self.url = url_parsed.path.decode('utf-8')
        self.headers = headers
        self.version = version
        self.method = method

        self.query_string = url_parsed.query.decode('utf-8') if url_parsed.query else None
        self.body = None
        self.parse_json = None
        self.parse_form = None
        self.parse_args = None

    @property
    def json(self):
        if not self.parse_json:
            try:
                self.parse_json = json.loads(self.body)
            except Exception as e:
                print(e)

        return self.parse_json

    @property
    def args(self):
        if not self.parse_args:
            try:
                self.parse_args = RequestParameters(parse_qs(self.query_string))
            except Exception as e:
                self.parse_args = RequestParameters()

        return self.parse_args
