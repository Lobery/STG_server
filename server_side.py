# -*- coding: UTF-8 -*-

from server_util import Server, ThreadServer
import os

class Handlers:

    @staticmethod
    def request(str):
        return str.upper()

    @staticmethod
    def login(username, password):
        with open('file/user.txt','r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            line = line.split(',')
            if len(line) != 2:
                continue
            _username = line[0]
            _password = line[1]
            if username == _username and password == _password:
                return 1
        return 0

    @staticmethod
    def register(username, password):
        # search if username already exist
        with open('file/user.txt','r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            line = line.split(',')
            if len(line) != 2:
                continue
            _username = line[0]
            if username == _username:
                return 0

        # add user
        lines.append(username + ',' + password + '\n')
        with open('file/user.txt', 'w') as f:
            f.writelines(lines)

        # add user info
        with open('file/userinfo/' + username + '.txt', 'w') as f:
            f.write('10\n100\n0\n0\n')

        return 1


    @staticmethod
    def searchCharacer(username):
        exist = False
        # search if username exist
        with open('file/user.txt','r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            line = line.split(',')
            if len(line) != 2:
                continue
            _username = line[0]
            if username == _username:
                exist = True
                break
        if not exist:
            return []
        files = os.listdir('file/userinfo/' + username)
        info = []
        for file in files:
            item = [file[:-4]]
            with open('file/userinfo/' + username + '/' + file, 'r') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                item.append(int(line))
            info.append(item)
        return info

if __name__ == '__main__':
    _server = ThreadServer('127.0.0.1', 8000, Handlers)
    _server.serve()