try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import sys
import subprocess
import time
import timeit

# Dictionary for helping with OCR
DICTIONARY = { 'i': '1', 'l': '1', 'O': '0', 'S': '5', 'b': '6', '?': '7', 'o': '0', 'Z': '2', 'z': '2'}

# Function for solution input and confirming input
def inputAndConfirm(data):
    subprocess.Popen(['adb', 'shell', 'input', 'text', data]).wait()
    subprocess.Popen(['adb', 'shell', 'input', 'keyevent', '66'])
    return

def solve():
    start_time = time.time()
    subprocess.Popen(['adb', 'shell', 'screencap', '-p', '/sdcard/dos.png']).wait()
    screen_time = time.time()
    game = Image.open('/sdcard/dos.png')
    width, height = game.size
    print(game.size)
    dos = game.crop((round(width/20), round(height/3.7), round(width/1.8), round(height/2.2)))
    # Full window
    #dos = game.crop(((width/27), (height/5.4), (width-(width/27)), (height/1.92)))
    dos.save('/sdcard/vision.png', 'PNG')
    screen = pytesseract.image_to_string(dos, lang='eng', config='-c tessedit_do_invert=0').replace('\n', ' ')
    ocr_time = time.time()
    unformattedPuzzle = screen.split(' ')
    print('Before format:')
    print(unformattedPuzzle)
    puzzle = []
    for item in unformattedPuzzle:
        if item and len(item) == 2:
            puzzle.append(item.translate(str.maketrans(DICTIONARY)).upper())
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
        inputAndConfirm(solutionBest[0])
    elif solutionMaybe:
        for solution in solutionMaybe:
            inputAndConfirm(solution)
    input_time = time.time()
    print('ELAPSED:')
    print('Screenshot time', (screen_time - start_time))
    print('OCR time', (ocr_time - screen_time))
    print('Solution time', (solution_time - ocr_time))
    print('Input time', (input_time - solution_time))
    print('Total', (time.time() - start_time))
    return
