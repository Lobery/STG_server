# -*- coding: UTF-8 -*-

import struct
from io import BytesIO
import socket
import threading

# search character
# para:(string)username
# return:(array[charactername, blood, bullet, level, experience])character_info
class SearchCharacterProtocol(object):

    # encode args
    def args_encode(self, username):
        # process request name
        name = 'searchCharacter'
        buff = struct.pack('!I', len(name))
        buff += name.encode()

        # process para(string)
        buff2 = struct.pack('!I', len(username))
        buff2 += username.encode()

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

        args["username"] = username
        return args

        
    # encode result
    def result_encode(self, array):
        # parse array length
        buff = struct.pack('!I', len(array))
        for item in array:
            name, blood, bullet, level, experience = item[0], item[1], item[2], item[3], item[4]
            # parse character name
            buff += struct.pack('!I', len(name))
            buff += name.encode()
            # parse blood
            buff += struct.pack('!I', blood)
            # parse bullet
            buff += struct.pack('!I', bullet)
            # parse level
            buff += struct.pack('!I', level)
            # parse experience
            buff += struct.pack('!I', experience)
        return buff
   
    # decode result
    def result_decode(self, connection):
        self.conn = connection

        # parse array length
        buff = self._read_all(4)
        length = struct.unpack('!I', buff)[0]
        info = []
        for i in range(length):
            # parse character name
            buff = self._read_all(4)
            length = struct.unpack('!I', buff)[0]
            buff = self._read_all(length)
            name = buff.decode()
            # parse blood
            buff = self._read_all(4)
            blood = struct.unpack('!I', buff)[0]
            # parse bullet
            buff = self._read_all(4)
            bullet = struct.unpack('!I', buff)[0]
            # parse level
            buff = self._read_all(4)
            level = struct.unpack('!I', buff)[0]
            # parse experience
            buff = self._read_all(4)
            experience = struct.unpack('!I', buff)[0]
            info.append([name, blood, bullet, level, experience])
        return info