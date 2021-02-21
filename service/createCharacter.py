# -*- coding: UTF-8 -*-

import struct
from io import BytesIO
import socket
import threading

# create character
# para:(string)username
#      (string)charactername
# return:(int)val:1:success
#                 0:fail
class CreateCharacterProtocol(object):

    # encode args
    def args_encode(self, username, characterName):
        # process request name
        name = 'createCharacter'
        buff = struct.pack('!I', len(name))
        buff += name.encode()

        # process para(string)
        buff2 = struct.pack('!I', len(username))
        buff2 += username.encode()

        # process para(string)
        buff2 += struct.pack('!I', len(characterName))
        buff2 += characterName.encode()

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

        # parse para:string
        buff = self._read_all(4)
        length = struct.unpack('!I', buff)[0]
        buff = self._read_all(length)
        username = buff.decode()

        # parse para:string
        buff = self._read_all(4)
        length = struct.unpack('!I', buff)[0]
        buff = self._read_all(length)
        characterName = buff.decode()

        args["username"] = username
        args["characterName"] = characterName
        return args

        
    # encode result
    def result_encode(self, val):
        # parse result
        buff = struct.pack('!I', val)
        return buff
   
    # decode result
    def result_decode(self, connection):
        self.conn = connection
        buff = self._read_all(4)
        val = struct.unpack('!I', buff)[0]
        return val