# -*- coding: UTF-8 -*-

import struct
from io import BytesIO
import socket
import threading

# An example
# para:(string)str
# return:(string)value
class RequestProtocol(object):

    # encode args
    def args_encode(self, str):
        # process request name
        name = 'request'
        buff = struct.pack('!I', len(name))
        buff += name.encode()

        # process para
        buff2 = struct.pack('!I', len(str))
        buff2 += str.encode()


        # process message length
        length = len(buff2)
        buff += struct.pack('!I', length)

        buff += buff2
        return buff

    # read bytes from message
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
                    # client close socket side
                    raise EOFError()
            return buff

    # decode args
    def args_decode(self, connection):
        args = {}
        self.conn = connection

        # parse msg length
        buff = self._read_all(4)
        length = struct.unpack('!I', buff)[0]

        # parse string
        buff = self._read_all(4)
        length = struct.unpack('!I', buff)[0]
        buff = self._read_all(length)
        name = buff.decode()

        args["str"] = name
        return args

        
    # encode result
    def result_encode(self, result):
        # parse string
        length = len(result)
        buff = struct.pack('!I', length)
        buff += result.encode()
        return buff
   
    # decode result
    def result_decode(self, connection):
        self.conn = connection

        # parse string
        buff = self._read_all(4)
        length = struct.unpack('!I', buff)[0]
        buff = self._read_all(length)
        message = buff.decode()

        return message