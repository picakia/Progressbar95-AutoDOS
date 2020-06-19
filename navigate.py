import subprocess
import time
import json
import re

import helpers
import HEX

def checkDirName(name):
    emptyList = ['<THE', 'DIRECT', '<INVALID']
    hexList = ['ENCRYPTED', 'YOU', 'NEED', 'WRONG']
    helpers.inputText([f'CD {name}'])
    screen = helpers.ocr(20, 4.55, 1.8)
    formatted = helpers.formatOcr(screen, False)
    print('Check Dir Name: ')
    print(formatted)
    for item in formatted:
        if item in hexList:
            HEX.solve()
            break
        if item in emptyList:
            return name[:-1] + '3'
    return False

def checkHex(foundStrings):
    hexList = ['WRONG', 'CODET', 'CODE']
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
    badFiles = ['UNKNOWN', 'README', 'README2', 'README3', 'MANUAL'] 
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
    if name in openFiles:
        nameType = 'open'
    if name in delFiles:
        nameType = 'del'
    if name in badFiles:
        nameType = 'bad'

    # Last letter fix
    lastLetter = name[-1:]
    if lastLetter == 'Z':
        name = name[:-1] + '2'
        nameType = 'check'
    return { 'name': name, 'nameType': nameType }

# Constant folders in game
def knownTree():
    return {
            'level': 0,
            'PROGRESSBAR': {
                'level': 1,
                'TEMP': 'unknown'
            },
            'DOCUMENTS': 'unknown',
            'BIN': 'unknown'
    }

def openDir(name=False, level=0):
    commands = [f'CD {name}', 'CLS', 'DIR']
    if not name:
        commands.pop(0)
    if level == 7:
        commands.pop()
        commands.pop()
    helpers.inputText(commands)
    screen = helpers.ocr()
    print('SCREEN')
    print(screen)
    formatted = helpers.formatOcr(screen, False)
    print('FORMATTED:')
    print(formatted)
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
            print('EMPTY: ', name)
            return thing
        if thing:
            if thing['name'] in dirs:
                thing['name'] = thing['name'][:-1] + '3'
            dirs[thing['name']] = thing['nameType']
    print('Found Dirs:')
    print(dirs)
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
        print('Empty folder!')
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
        if value == 'unknown':
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
    print('CURRENT DIR')
    print(currentDir)
    if currentDir != 'empty':
        explored = explore(currentDir, currentDir['level']+1, False)
        print(json.dumps(explored, indent=2))
    print('ELAPSED explore:')
    print('Total', (time.time() - start_time))
    helpers.inputText(['FINISHED!'])
    return
