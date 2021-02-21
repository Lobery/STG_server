import os
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
            item.append(line)
        info.append(item)
    return info


print searchCharacer("nete22ase1")