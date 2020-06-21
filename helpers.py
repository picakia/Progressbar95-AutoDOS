from PIL import Image
import subprocess
import time
from navigate import checkTypeOfItem

resolution = subprocess.run(['adb', 'shell', 'wm', 'size'], universal_newlines=True, stdout=subprocess.PIPE)
width, height = resolution.stdout[15:-1].split('x')
width = int(width)
height = int(height)
print('Get device resolution:', width, height)

# OCR formatter
def formatOcr(string, replace='dirs', lenght=40):
    dictionary = { 'n': 'M', '?': '!', '�': 'A' }
    if replace == 'hex':
        dictionary = { 'I': '1', 'i': '1', 'l': '1', 'O': '0', 'S': '5', 'b': '6', '?': '7', 'o': '0', 'Z': '2', 'z': '2', 'g': '8', 'n': 'A', 'q': '4', '�': 'A', '|': '0'}
    arrayToFormat = string.replace('\n', ' ').split(' ')
    formatted = []
    for item in arrayToFormat:
        if item and len(item) > 1:
            if len(item) > lenght:
                # Three char fix
                if item[-2:] == 'Ol' or item[-2:] == 'ol':
                    item = item[:1] + '0'
                else:
                    item = item[:1] + item[-1:]
            if replace == 'none':
                formatted.append(item.upper().strip())
            else:
                formatted.append(item.translate(str.maketrans(dictionary)).upper().strip())
    print(f'[helpers.py] Formatted output {replace}:\n', formatted)
    return formatted

# Function for solution input and confirming input
def inputText(data):
    for command in data:
        subprocess.Popen(['adb', 'shell', 'input', 'text', command.replace(' ', '\ ')]).wait()
        subprocess.Popen(['adb', 'shell', 'input', 'keyevent', '66']).wait()
    return

# Get what matters from screenshot
def ocr(divideLeft=20, divideTop=4.55, divideRight=3.2, divideBottom=2.1):
    start_time = time.time()
    screenShot = subprocess.Popen(['adb', 'shell', 'screencap', '/sdcard/dos.raw']).wait()
    file = open('/sdcard/dos.raw', 'rb')
    raw = file.read()
    file.close()
    game = Image.frombuffer('RGBA', (1080,2160), raw, 'raw', 'RGBA', 0, 1)
    dos = game.crop((round(width/divideLeft), round(height/divideTop), round(width/divideRight), round(height/divideBottom)))
    #game.save('/sdcard/vision.png', 'PNG')
    dos.save('/sdcard/vision.ppm', 'PPM')
    ocrad = subprocess.run(["ocrad", "--scale=2", "/sdcard/vision.ppm"], universal_newlines=True, errors='replace', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    vision = ocrad.stdout
    print('[helpers.py] Vision:\n', vision)
    print('[helpers.py] OCR time:\n', (time.time()-start_time))
    return vision

# Constant folders in game
def getKnownTree():
    inputText(['CLS', 'DIR'])
    screen = ocr()
    formatted = formatOcr(screen)
    dirs = { 'level': 0 }
    for item in formatted:
        thing = checkTypeOfItem(item)
        if not thing:
            continue
        if thing['name'] == 'PROGRESSBAR':
            dirs[thing['name']] = {
                'level': 1,
                'COLORCODE': 'enter',
                'SYSCODE': 'enter',
                'TEMP': 'unknown'
            }
        elif thing['name'] == 'PROGRAMS':
            #dirs[thing['name']] = {
            #    'level': 1,
            #    'LATIN': {
            #        'CODEX': 'enter'
            #    }
            #}
            # No codex code support currently
            dirs[thing['name']] = 'empty'
        else:
            if thing['name'] in dirs:
                thing['name'] = thing['name'][:-1] + '3'
            dirs[thing['name']] = thing['nameType']
    return dirs

