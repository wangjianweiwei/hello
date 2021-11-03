# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/11/1 8:26 下午
"""
import asyncio
from asyncio import transports
from typing import Optional
from httptools import HttpRequestParser

from hello.request import Request
from hello.log import log


class HttpProtocol(asyncio.Protocol):

    def __init__(self, loop, request_handle):
        self.loop = loop
        self.request_handle = request_handle
        self.parse: HttpRequestParser = HttpRequestParser(self)
        self.url = None
        self.headers = list()
        self.request = None
        self.transport = None  # type: transports.BaseTransport

    def connection_made(self, transport: transports.BaseTransport) -> None:
        self.transport = transport
        super(HttpProtocol, self).connection_made(transport)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        super(HttpProtocol, self).connection_lost(exc)

    def data_received(self, data: bytes) -> None:
        self.parse.feed_data(data)

    def eof_received(self) -> Optional[bool]:
        return True

    def on_url(self, url):
        self.url = url

    def on_header(self, name: bytes, value: bytes):
        # TODO: 校验请求头中Content-Length
        self.headers.append((name.decode(), value.decode()))

    def on_headers_complete(self):
        self.request = Request(url_bytes=self.url, headers=dict(self.headers), version=self.parse.get_http_version(),
                               method=self.parse.get_method().decode())

    def on_body(self, body):
        self.request.body = body

    def on_message_complete(self):
        self.loop.create_task(self.request_handle(self.request, self.write_response))

    def write_response(self, response):
        self.transport.write(response.output(self.request.version))
        self.transport.close()


def server(host, port, request_handle):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server_coroutine = loop.create_server(
        protocol_factory=lambda: HttpProtocol(loop=loop, request_handle=request_handle), host=host, port=port)
    log.info('Goin\' Fast @ http://{}:{}'.format(host, port))
    http_server = loop.run_until_complete(server_coroutine)

    try:
        loop.run_forever()
    except Exception as e:
        pass
    finally:
        log.info("Stop")
        http_server.close()
        loop.run_until_complete(http_server.wait_closed())
        loop.close()
