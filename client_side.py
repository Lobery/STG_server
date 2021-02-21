# -*- coding: UTF-8 -*-

from client_util import ClientStub
from client_util import Channel

# initialize connection
channel = Channel('127.0.0.1', 8000)
stub = ClientStub(channel)


try:
    val = stub.searchCharacter("neteeease1")
except:
    pass
else:
    print(val)

# close connection
stub.conn.close()