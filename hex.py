try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import sys
import subprocess
import time
import timeit

print('Open game')
subprocess.Popen(['am', 'start', '--activity-single-top', '-n', 'com.spookyhousestudios.progressbar95/com.ansca.corona.CoronaActivity'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
#subprocess.Popen(['adb', 'devices'], stdout=subprocess.DEVNULL).wait()
start_time = time.time()
subprocess.Popen(['adb', 'shell', 'screencap', '-p', '/sdcard/dos.png']).wait()
screen_time = time.time()
game = Image.open('/sdcard/dos.png')
width, height = game.size
print(game.size)
dos = game.crop(((width/27), (height/5.4), (width-(width/27)), (height/1.92)))
dos.save('/sdcard/vision.png', 'PNG')
screen = pytesseract.image_to_string(dos, lang='eng', config='-c tessedit_do_invert=0').replace('\n', ' ')
ocr_time = time.time()
unformattedPuzzle = screen.split(' ')
print('Before format:')
print(unformattedPuzzle)
puzzle = []
for item in unformattedPuzzle:
    if item and len(item) == 2:
        puzzle.append(item.replace('i', '1').replace('l', '1').replace('O', '0').replace('S', '5').replace('b', '6').replace('?', '7').upper())
print('FORMATTED:')
print(puzzle)
solutionBest = []
solutionMaybe = []
solutionLow = []
for number in puzzle:
    if number != '':
        if puzzle.count(number) > 4:
            if number not in solutionBest:
                solutionBest.append(number)
        if puzzle.count(number) == 4:
            if number not in solutionMaybe:
                solutionMaybe.append(number)
        if puzzle.count(number) == 3:
            if number not in solutionLow:
                solutionLow.append(number)
solution_time = time.time()
print('SOLUTION:')
print('Best: ', solutionBest, ' Maybe: ', solutionMaybe, ' Low: ', solutionLow)
if solutionBest:
    subprocess.Popen(['adb', 'shell', 'input', 'text', solutionBest[0]]).wait()
    subprocess.Popen(['adb', 'shell', 'input', 'keyevent', '66']).wait()
elif solutionMaybe:
    subprocess.Popen(['adb', 'shell', 'input', 'text', solutionMaybe[0].upper()]).wait()
    subprocess.Popen(['adb', 'shell', 'input', 'keyevent', '66']).wait()
input_time = time.time()
print('ELAPSED:')
print('Screenshot time', (screen_time - start_time))
print('OCR time', (ocr_time - screen_time))
print('Solution time', (solution_time - ocr_time))
print('Input time', (input_time - solution_time))
print('Total', (time.time() - start_time))
#subprocess.Popen(['am', 'start', '--activity-single-top', 'com.termux/com.termux.app.TermuxActivity'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
