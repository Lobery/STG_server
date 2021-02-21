# -*- coding: UTF-8 -*-

import struct
from io import BytesIO
import socket
import threading

# service provided by server
from service.request import RequestProtocol
from service.login import LoginProtocol
from service.register import RegisterProtocol
from service.searchCharacter import SearchCharacterProtocol

# connect with client
class Channel(object):

    # register host and port
    def __init__(self, host, port):
        self.host = host
        self.port = port

    # get connected client
    def get_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock


# client side to perform RPC
class ClientStub(object):

    # initialize
    def __init__(self, channel):
        self.channel = channel
        self.conn = self.channel.get_connection()

    # process para
    # send by net
    # process return value
    def process(self, args, proto):
        self.conn.sendall(args)
        result = proto.result_decode(self.conn)
        return result


    # perform reqeust service
    def request(self, str):
        proto = RequestProtocol()
        args = proto.args_encode(str)
        return self.process(args, proto)

    # perform login service
    def login(self, username, password):
        proto = LoginProtocol()
        args = proto.args_encode(username, password);
        return self.process(args, proto)

    # perform register service
    def register(self, username, password):
        proto = RegisterProtocol()
        args = proto.args_encode(username, password);
        return self.process(args, proto)

    # perform search character service
    def searchCharacter(self, username):
        proto = SearchCharacterProtocol()
        args = proto.args_encode(username);
        return self.process(args, proto)