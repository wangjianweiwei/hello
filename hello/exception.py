# -*- coding: utf-8 -*-
from traceback import format_exc

from hello.response import text


class HelloException(Exception):
    status_code = None

    def __init__(self, message, status_code=None):
        super(HelloException, self).__init__(message)
        if status_code is not None:
            self.status_code = status_code


class NotFound(HelloException):
    status_code = 404


class InvalidUsage(HelloException):
    status_code = 400


class ServerError(HelloException):
    status_code = 500


class ExceptionHandle:

    def __init__(self, app):
        self.app = app
        self.handlers = {}

    def add(self, exc, handler):
        self.handlers[type(exc)] = handler

    def response(self, request, exc):
        handler = self.handlers.get(type(exc), self.default)
        response = handler(request=request, exc=exc)

        return response

    def default(self, request, exc):
        if issubclass(type(exc), HelloException):
            return text("Error: {}".format(exc), status=getattr(exc, 'status_code', 500))
        # elif self.sanic.debug:
        #     return text("Error: {}\nException: {}".format(exc, format_exc()), status=500)
        else:
            print(exc)
            return text("An error occurred while generating the request", status=500)
