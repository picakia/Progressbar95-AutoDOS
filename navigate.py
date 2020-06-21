import subprocess
import time
import json
import re

import helpers
import HEX
import codes

def checkDir(name):
    invalidList = ['<INVALID', '{INVALID', '{INUALID']
    hexList = ['ENCRYPTED', 'NEED', 'WROMG', 'WRONG', '[HEX]', '[X]', 'VIEWER', 'UIEWER']

    validDir = True
    screen = helpers.ocr(20, 4, 1.8, 2.1)
    #screen = helpers.ocr(5.5, 4, 1.35, 2.1)
    formatted = helpers.formatOcr(screen, 'none')
    print(f'[navigate.py] CheckDir {name}:\n', formatted)
    for item in formatted:
        if item in hexList:
            HEX.solve()
            return (name, validDir)
    for item in formatted:
        if item in invalidList:
            print('[navigate.py] BAD folder', name)
            if name[:-1] == '2':
                validDir = 'changed'
                name = name[:-1] + '3'
            else:
                validDir = False
            return (name, validDir)
    return (name, validDir)

def goBack(HEX=False):
    command = ['CD..']
    if HEX:
        command = ['X']
    helpers.inputText(command)

def checkTypeOfItem(name):
    emptyList = ['<THE', '{THE', 'DIRECT', '<INVALID','{INVALID']
    blacklist = ['TXT', 'EXE', '<', '>', ':', '/', '.', '-', '{', '}']
    fixingList = {'MSC': 'MISC'}
    openFiles = ['BONUS', 'EASTEREGG']
    delFiles = ['CHEATS']
    badFiles = ['UNKNOWN', 'README', 'README2', 'README3', 'README4', 'MANUAL']

    nameType = 'unknown'
    
        # Double char fix
        #match = re.search(r'((\w)\2{1,})', name)
        #if match:
        #    name = name.replace(match.group(1), match.group(1)[:1])
        #else:
        #    return False
    
    # FixingList fixes 
    for key, value in fixingList.items():
        if name == key:
            name = value

    # Check if directory is empty
    if name in emptyList:
         return 'empty'
    # Check blacklist
    for item in blacklist:
        if item in name:
            return False
    # Last letter fix
    lastLetter = name[-1:]
    if lastLetter == 'Z':
        name = name[:-1] + '2'
    if name in openFiles:
        nameType = 'open'
    if name in delFiles:
        nameType = 'del'
    if name in badFiles:
        nameType = 'bad'

    return { 'name': name, 'nameType': nameType }

def openDir(name=False, level=0):
    if name:
        helpers.inputText([f'CD {name}'])
        name, valid = checkDir(name)
        if not valid:
            return 'invalid'
        if valid == 'changed':
            helpers.inputText([f'CD {name}'])
    if level == 6:
        return 'empty'

    helpers.inputText(['CLS', 'DIR'])
    screen = helpers.ocr()
    formatted = helpers.formatOcr(screen)
    print(f'[navigate.py] Opened DIR {name}\n', formatted)
    dirs = { 'level': level }
    for item in formatted:
        thing = checkTypeOfItem(item)
        if thing == 'empty':
            print('[navigate.py] Dir empty:', name)
            return thing
        if thing:
            if thing['name'] in dirs:
                thing['name'] = thing['name'][:-1] + '3'
            dirs[thing['name']] = thing['nameType']
    print(f'[navigate.py] Found Dirs in {name}:\n', dirs)
    return dirs

def openFile(name, method):
    if method == 'open':
        helpers.inputText([name])
    if method == 'del':
        helpers.inputText([f'DEL {name}.TXT'])
    if method == 'enter':
        codes.enter(name)
    return

def explore(currentDir, level=0, recur=True):
    explore_time = time.time()
    if currentDir == 'empty':
        print('[navigate.py] Empty starting folder!')
        return
    for key, value in currentDir.items():
        if value == 'empty':
            currentDir[key] = value
            if level != 1:
                goBack()
        elif value == 'unknown':
            newDir = openDir(key, level)
            if newDir != 'empty':
                currentDir[key] = newDir
                explore(newDir, (level+1))
            else:
                currentDir[key] = newDir
                goBack()
        elif isinstance(value, dict):
            helpers.inputText([f'CD {key}'])
            explore(value, level)
        else:
            openFile(key, value)
    if recur:
        goBack()
    return currentDir

def start(current=False, level=0, syscode=False):
    start_time = time.time()
    currentDir = 'empty'
    if current:
        currentDir = openDir(False, level)
    else:
        currentDir = helpers.getKnownTree()

    print('[navigate.py] Dir to explore:\n', currentDir)
    if currentDir != 'empty':
        explored = explore(currentDir, currentDir['level']+1, False)
        print('[navigate.py] EXPLORED TREE:\n', json.dumps(explored, indent=2))
    print('[navigate.py] ELAPSED explore:')
    print('[navigate.py] Total:', round((time.time() - start_time), 4))
    helpers.inputText(['FINISHED!'])
    return
