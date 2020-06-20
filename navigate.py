import subprocess
import time
import json
import re

import helpers
import HEX

# Constant folders in game
def knownTree():
    return {
            'level': 0,
            'PROGRESSBAR': {
                'level': 1,
                #'COLORCODE': 'enter',
                #'SYSCODE': 'enter',
                'TEMP': 'unknown'
            },
            'DOCUMENTS': 'unknown',
            'BIN': 'unknown',
            'PROGRAMS': 'empty',
            'README': 'bad'
    }

def checkDirName(name):
    emptyList = ['<THE', 'DIRECT', '<INVALID']
    hexList = ['ENCRYPTED', 'YOU', 'NEED', 'WRONG']
    helpers.inputText([f'CD {name}'])
    screen = helpers.ocr(20, 4.55, 1.8)
    formatted = helpers.formatOcr(screen, False)
    print(f'[navigate.py] CheckDirName {name}:\n', formatted)
    for item in formatted:
        if item in hexList:
            HEX.solve()
            break
        if item in emptyList:
            return name[:-1] + '3'
    return False

def checkHex(foundStrings):
    hexList = ['WRONG', 'YOU', 'NEED', '[HEX]']
    for string in foundStrings:
        if string in hexList:
            return True
    return False

def goBack(HEX=False):
    command = ['CD..']
    if HEX:
        command = ['X']
    helpers.inputText(command)

def checkFolder(name):
    emptyList = ['<THE', 'DIRECT', '<INVALID']
    blacklist = ['TXT', 'EXE', '<', '>', ':', '/', '.', '-']
    fixingList = ['PR', 'UNKNOUWN', 'DOCCS', 'READHE', 'PROGRESS']
    openFiles = ['BONUS', 'EASTEREGG']
    delFiles = ['CHEATS']
    badFiles = ['UNKNOWN', 'README', 'README2', 'README3', 'README4', 'MANUAL'] 
    nameType = 'unknown'
    check = False
    # Other fixes
    if name in fixingList:
        # Double char fix
        match = re.search(r'((\w)\2{1,})', name)
        if match:
            name = name.replace(match.group(1), match.group(1)[:1])
        else:
            return False
    # First letter fix
    firstLetter = name[:2]
    if firstLetter == 'TF' or firstLetter == '1F':
        name = '!' + name[1:]
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
        nameType = 'check'
    # TEMFP fix
    lastFP = name[-2:]
    if lastFP == 'FP':
        name = name[:-2] + 'P'
    if name in openFiles:
        nameType = 'open'
    if name in delFiles:
        nameType = 'del'
    if name in badFiles:
        nameType = 'bad'

    return { 'name': name, 'nameType': nameType }

def openDir(name=False, level=0):
    commands = [f'CD {name}', 'CLS', 'DIR']
    if not name:
        commands.pop(0)
    if level == 7:
        commands.pop()
        commands.pop()
    if not commands:
        helpers.inputText(['CD..'])
        return 'empty'
    helpers.inputText(commands)
    screen = []
    if level == 7:
        screen = helpers.ocr(5.5, 4, 1.35, 2.1)
    else:
        screen = helpers.ocr()
    formatted = helpers.formatOcr(screen, False)
    print(f'[navigate.py] Opened DIR {name}:\n', formatted)
    dirs = { 'level': level }
    isHex = checkHex(formatted)
    if isHex:
        HEX.solve()
        if level == 7:
            return 'empty'
        return openDir(False, level)
    if level == 7:
        return 'empty'
    for item in formatted:
        thing = checkFolder(item)
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
    return

def explore(currentDir, level=0, recur=True):
    explore_time = time.time()
    if currentDir == 'empty':
        print('[navigate.py] Empty starting folder!')
        return
    for key, value in currentDir.items():
        dirToOpen = key
        if value == 'check':
            newName = checkDirName(dirToOpen)
            if newName:
                dirToOpen = newName
            else:
                dirToOpen = False
            value = 'unknown'
            if level == 7:
                value = 'empty'
        if value == 'empty':
            currentDir[key] = value
            goBack()
        elif value == 'unknown':
            newDir = openDir(dirToOpen, level)
            if newDir != 'empty':
                currentDir[key] = newDir
                explore(newDir, (level+1))
            else:
                currentDir[key] = newDir
                goBack()
        else:
            openFile(key, value)
    if recur:
        goBack()
    return currentDir

def start(current=False, level=0):
    start_time = time.time()
    currentDir = knownTree()['PROGRESSBAR']
    if current:
        currentDir = openDir(False, level)
    print('[navigate.py] Dir to explore:\n', currentDir)
    if currentDir != 'empty':
        explored = explore(currentDir, currentDir['level']+1, False)
        print('[navigate.py] EXPLORED TREE:\n', json.dumps(explored, indent=2))
    print('[navigate.py] ELAPSED explore:')
    print('[navigate.py] Total:', round((time.time() - start_time), 4))
    helpers.inputText(['FINISHED!'])
    return
