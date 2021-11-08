# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/11/2 2:26 下午
"""
import re
from typing import List
from collections import namedtuple

from hello.exception import NotFound, InvalidUsage

Route = namedtuple("Route", ["handler", "methods", "pattern", "parameters"])
Parameter = namedtuple("Parameter", ["name", "cast"])


class Router:
    routes = None
    regex_types = {
        "string": (None, r"\w+"),
        "int": (int, r"\d+"),
        "number": (float, r"[0-9\.]+"),
        "alpha": (None, r"[A-Za-z]+"),
    }

    def __init__(self):
        self.routes: List[Route] = []

    def add(self, url, methods, handle):
        methods_dict = dict().fromkeys(methods) if methods else None

        parameters = []

        def add_parameter(match: re.Match):
            parts = match.group(1).split(":")
            if len(parts) == 2:
                parameter_name, parameter_pattern = parts
            else:
                parameter_name = parts[0]
                parameter_pattern = "string"

            parameter_regex = self.regex_types.get(parameter_pattern)
            if parameter_regex:
                parameter_type, parameter_pattern = parameter_regex
            else:
                parameter_type = None

            parameter = Parameter(name=parameter_name, cast=parameter_type)
            parameters.append(parameter)

            return f"({parameter_pattern})"

        pattern_string = re.sub("<.+?>", add_parameter, url)
        pattern = re.compile(f"^{pattern_string}$")

        route = Route(handler=handle, methods=methods_dict, pattern=pattern, parameters=parameters)
        self.routes.append(route)

    def get(self, request):
        args = []
        kwargs = {}
        route = None
        for route in self.routes:
            if match := route.pattern.match(request.url):
                for index, parameter in enumerate(route.parameters, 1):
                    value = match.group(index)
                    kwargs[parameter.name] = parameter.cast(value) if parameter.cast else value
                break

        if route:
            if route.methods and request.method not in route.methods:
                raise InvalidUsage(f"Method {request.method} not allowed for URL {request.url}", status_code=405)

            return route.handler, args, kwargs
        else:
            raise NotFound("Requested URL {} not found".format(request.url))
