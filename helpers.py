from PIL import Image
import pytesseract
import subprocess
import time

# OCR formatter
def formatOcr(string, replace=True, split=True, lenght=40):
    dictionary = { 'i': '1', 'l': '1', 'O': '0', 'S': '5', 'b': '6', '?': '7', 'o': '0', 'Z': '2', 'z': '2', 'g': '8', 'n': 'A'}
    if not split:
        return string.translate(str.maketrans(dictionary)).upper().strip()
    arrayToFormat = string.split(' ')
    formatted = []
    for item in arrayToFormat:
        if item:
            if len(item) > lenght:
                # Three char fix
                item = item[:1] + item[-1:]
            if replace:
                formatted.append(item.translate(str.maketrans(dictionary)).upper().strip())
            else:
                formatted.append(item.upper().strip())
    return formatted

# Function for solution input and confirming input
def inputText(data):
    for command in data:
        subprocess.Popen(['adb', 'shell', 'input', 'text', command.replace(' ', '\ ')]).wait()
        subprocess.Popen(['adb', 'shell', 'input', 'keyevent', '66']).wait()
    return

# Get what matters from screenshot
def ocr(divideLeft=20, divideTop=4.55, divideRight=3.2, divideBottom=2.1):
    subprocess.Popen(['adb', 'shell', 'screencap', '-p', '/sdcard/dos.png']).wait()
    game = Image.open('/sdcard/dos.png')
    width, height = game.size
    dos = game.crop((round(width/divideLeft), round(height/divideTop), round(width/divideRight), round(height/divideBottom)))
    ocr_time = time.time()
    dos.save('/sdcard/vision.png', 'PNG')
    vision = pytesseract.image_to_string(dos, lang='eng', config='-c tessedit_do_invert=0 --psm 4').replace('\n', ' ')
    print('[helpers.py] OCR time:', round((time.time() - ocr_time), 4))
    return vision

