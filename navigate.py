import subprocess
import time

import helpers

def goBack():
    helpers.inputText(['CD..'])

def checkFolder(name):
    emptyList = ['<THE', 'DIRECTORY', 'IS', '<INVALID']
    blacklist = ['TXT', 'EXE', '<', '>', ':', '/']
    openFiles = ['BONUS', 'EASTEREGG']
    delFiles = ['CHEATS']
    badFiles = ['UNKNOWN', 'README', 'README2', 'README3'] 
    nameType = 'unknown'
    check = False
    # Check if directory is empty
    for item in emptyList:
        if name in item:
            return 'empty'
    # Check blacklist
    for item in blacklist:
        if item in name:
            return False
    if len(name) < 3:
        return False
    # Last letter fix
    lastLetter = name[-1:]
    if lastLetter == 'Z':
        name = name[:-1] + '2'
        check = True
    # First letter fix
    firstLetter = name[:1]
    if firstLetter == 'T':
        name = '!' + name[1:]
    if name in openFiles:
        nameType = 'open'
    if name in delFiles:
        nameType = 'del'
    if name in badFiles:
        nameType = 'bad'

    if check:
        valid = True
        helpers.inputText([f'CD {name}'])
        screen = helpers.ocr()
        formatted = helpers.formatOcr(screen, False)
        print(formatted)
        for item in formatted:
            for item2 in emptyList:
                if item in item2:
                    name = name[:-1] + '3'
                    valid = False
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
    formatted = helpers.formatOcr(screen, False)
    print('FORMATTED:')
    print(formatted)
    dirs = { 'level': level }
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
        helpers.inputText([f'DEL {name}'])
    return

def explore(folderTree, level=0):
    explore_time = time.time()
    if folderTree == 'empty':
        print('Empty folder!')
        return
    for key, value in folderTree.items():
        if value == 'unknown':
            newDir = openDir(key, level)
            if newDir != 'empty':
                folderTree[key] = newDir
                explore(newDir, level+1)
            else:
                folderTree[key] = newDir
                goBack()
        else:
            openFile(key, value)
    goBack()
    return folderTree

def start():
    start_time = time.time()
    folderTree = knownTree()
    currentDir = openDir()
    explored = explore(currentDir)
    print(explored)
    print('ELAPSED explore:')
    print('Total', (time.time() - start_time))
    return
