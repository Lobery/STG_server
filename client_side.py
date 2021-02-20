# -*- coding: UTF-8 -*-

from util import ClientStub
from util import Channel

# initialize connection
channel = Channel('127.0.0.1', 8000)
stub = ClientStub(channel)


try:
    val = stub.request("abc")
except:
    pass
else:
    print(val)

# close connection
stub.conn.close()