# -*- coding: UTF-8 -*-

from util import Server, ThreadServer


class Handlers:

    @staticmethod
    def request(str):
        return str.upper()


if __name__ == '__main__':
    _server = ThreadServer('127.0.0.1', 8000, Handlers)
    _server.serve()