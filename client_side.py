# -*- coding: UTF-8 -*-

from client_util import ClientStub
from client_util import Channel
import sys




if __name__ == '__main__':
    # initialize connection
    channel = Channel('127.0.0.1', 8000)
    stub = ClientStub(channel)
    type = sys.argv[1]
    args = sys.argv[2].split(',')
    try:
        if type == 'login':
            username, password = args[0], args[1]
            val = stub.login(username, password)
        elif type == 'register':
            username, password = args[0], args[1]
            val = stub.register(username, password)
        elif type == 'searchCharacter':
            username = args[0]
            val = stub.searchCharacter(username)
        elif type == 'createCharacter':
            username, characterName = args[0], args[1]
            val = stub.createCharacter(username, characterName)
        elif type == 'updateCharacter':
            username, characterName = args[0], args[1]
            blood, bullet, level, experience = int(args[2]), int(args[3]), int(args[4]), int(args[5])
            val = stub.updateCharacter(username, characterName,
                                       blood, bullet, level, experience)
    except:
        val = 'failure'
    with open('result.txt', 'w') as f:
        f.write(str(val))
    print(val)
    # close connection
    stub.conn.close()