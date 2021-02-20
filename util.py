# -*- coding: UTF-8 -*-

import struct
from io import BytesIO
import socket
import threading

# service provided by server
from service.request import RequestProtocol

# process different methods
class MethodProtocol(object):

    # initialize connection
    def __init__(self, connection):
        self.conn = connection

    # read from message
    def _read_all(self, size):
        if isinstance(self.conn, BytesIO):
            buff = self.conn.read(size)
            return buff
        else:
            have = 0
            buff = b''
            while have < size:
                chunk = self.conn.recv(size - have)
                buff += chunk
                l = len(chunk)
                have += l
                if l == 0:
                    raise EOFError()
            return buff

    # decode string
    # string is encode by [string_length:string_value]
    def get_string_value(self):
        # get string length
        buff = self._read_all(4)
        length = struct.unpack('!I', buff)[0]
        # get string value
        buff = self._read_all(length)
        return buff.decode()


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

# RPC server
class Server(object):

    # initialize RPC connection
    def __init__(self, host, port, handlers):
        # create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set socket reuse address
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind address
        sock.bind((host, port))
        self.host = host
        self.port = port
        self.sock = sock
        self.handlers = handlers

    # start server to provide RPC service
    def serve(self):
        self.sock.listen(128)
        print("Server starts listening...")

        # receive connection from client
        while True:
            client_sock, client_addr = self.sock.accept()
            print('Connect with client:%s' % str(client_addr))

            # ServerStub performs clients' request
            stub = ServerStub(client_sock, self.handlers)
            try:
                while True:
                    stub.process()
            except EOFError:
                print('Client has shut down connection')
                client_sock.close()


# multi-thread RPC server
class ThreadServer(object):

    # initialize
    def __init__(self, host, port, handlers):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        self.host = host
        self.port = port
        self.sock = sock
        self.handlers = handlers

    # server provide service
    def serve(self):
        self.sock.listen(128)
        print("Server starts listening...")

        while True:
            client_sock, client_addr = self.sock.accept()
            print('Connect with client:%s' % str(client_addr))

            t = threading.Thread(target=self.handle, args=(client_sock,))

            # open child thread
            t.start()

    # child thread performs request
    def handle(self, client_sock):
        stub = ServerStub(client_sock, self.handlers)
        try:
            while True:
                stub.process()
        except EOFError:
            print('客户端关闭了连接')
            client_sock.close()


# client side to perform RPC
class ClientStub(object):

    # initialize
    def __init__(self, channel):
        self.channel = channel
        self.conn = self.channel.get_connection()

    # process para
    # send by net
    # process return value
    def process(self, str, proto):
        args = proto.args_encode(str)
        self.conn.sendall(args)
        result = proto.result_decode(self.conn)
        return result


    # perform reqeust service
    def request(self, str):
        proto = RequestProtocol()
        return self.process(str, proto)

# server side to perform RPC
class ServerStub(object):

    # initialize
    def __init__(self, connection, handlers):
        self.conn = connection
        self.method_proto = MethodProtocol(self.conn)
        self.process_map = {
            'request' : self._process_request,
        }
        self.protocol_map = {
            'request' : RequestProtocol(),
        }
        self.handlers = handlers
        self.name = ''

    # connect with client and finish RPC
    def process(self):
        # parse request name
        self.name = self.method_proto.get_string_value()

        # call request function
        _process = self.process_map[self.name]
        _process()


    # process request
    def _process_request(self):
        proto = self.protocol_map[self.name]

        # parse paras
        args = proto.args_decode(self.conn)

        # call method
        val = self.handlers.request(**args)
        ret_message = proto.result_encode(val)
        self.conn.sendall(ret_message)


