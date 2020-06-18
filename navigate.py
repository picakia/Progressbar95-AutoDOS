import subprocess
import time
import json
import re

import helpers
import HEX

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
    hexList = ['ENCRYPTED', 'DIRE', 'YOU', 'NEED', 'WRONG']
    blacklist = ['TXT', 'EXE', '<', '>', ':', '/', '.']
    fixingList = ['PR', 'UNKNOUWN', 'DOCCS']
    openFiles = ['BONUS', 'EASTEREGG']
    delFiles = ['CHEATS']
    badFiles = ['UNKNOWN', 'README', 'README2', 'README3'] 
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
    # Last letter fix
    lastLetter = name[-1:]
    if lastLetter == 'Z':
        name = name[:-1] + '2'
        check = True
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
        check = False

    if check:
        valid = True
        helpers.inputText([f'CD {name}'])
        screen = helpers.ocr(20, 4.55, 1.8)
        formatted = helpers.formatOcr(screen, False)
        print(formatted)
        for item in formatted:
            if item in hexList:
                HEX.solve()
                break
            if item in emptyList:
                name = name[:-1] + '3'
                valid = False
                break
        if valid:
            goBack()
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
        return openDir(False, level)
    for item in formatted:
        thing = checkFolder(item)
        if thing == 'empty':
            print('EMPTY: ', name)
            return thing
        if thing:
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

def explore(currentDir, level=0):
    explore_time = time.time()
    if currentDir == 'empty':
        print('Empty folder!')
        return
    for key, value in currentDir.items():
        if value == 'unknown':
            newDir = openDir(key, level)
            if newDir != 'empty':
                currentDir[key] = newDir
                explore(newDir, (level+1))
            else:
                currentDir[key] = newDir
                goBack()
        else:
            openFile(key, value)
    goBack()
    return currentDir

def start(current=False):
    start_time = time.time()
    currentDir = knownTree()['PROGRESSBAR']
    if current:
        currentDir = openDir()
    explored = explore(currentDir, 1)
    print(json.dumps(explored, indent=2))
    print('ELAPSED explore:')
    print('Total', (time.time() - start_time))
    helpers.inputText(['FINISHED!'])
    return
