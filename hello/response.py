# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/11/1 9:02 下午
"""
import ujson

STATUS_CODES = {
    200: 'OK',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
}


class HttpResponse:

    def __init__(self, body: str = None, status: int = 200, headers: dict = None, content_type="text/plain",
                 body_bytes=b''):
        self.status = status
        self.headers = headers or dict()
        self.content_type = content_type

        if body is not None:
            self.body = body.encode("utf-8")
        else:
            self.body = body_bytes

    def output(self, version="1.1", keep_alive=False, keep_alive_timeout=None):
        additional_headers = []
        if keep_alive and keep_alive_timeout is not None:
            additional_headers = [b'Keep-Alive: timeout=', str(keep_alive_timeout).encode('utf-8'), b'\r\n']

        for k, v in self.headers.items():
            additional_headers.append(f"{k}: {v}\r\n".encode('utf-8'))

        return b''.join([
                            'HTTP/{} {} {}\r\n'.format(version, self.status,
                                                       STATUS_CODES.get(self.status, 'FAIL')).encode(),
                            b'Content-Type: ', self.content_type.encode(), b'\r\n',
                            b'Content-Length: ', str(len(self.body)).encode(), b'\r\n',
                            b'Connection: ', ('keep-alive' if keep_alive else 'close').encode(), b'\r\n',
                        ] + additional_headers + [
                            b'\r\n',
                            self.body,
                        ])


def json(body, status=200, headers=None):
    return HttpResponse(ujson.dumps(body), headers=headers, status=status, content_type="application/json")


def text(body, status=200, headers=None):
    return HttpResponse(body, status=status, headers=headers, content_type="text/plain")
