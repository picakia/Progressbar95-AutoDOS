import subprocess
import time

# Custom modules
import helpers

def enter(syscode):
    start_time = time.time()
    screen = helpers.ocr(1.16, 4.6, 1.05, 4.1)
    ocr_time = time.time()
    print('SCREEN:')
    print(screen)
    screen = screen.translate(str.maketrans(helpers.dictionary())).upper().strip()
    print('FORMATTED:')
    print(screen)
    commands = ['CD PROGRESSBAR', 'COLORCODE', screen]
    if syscode:
        commands.extend(['SYSCODE', syscode]);
    helpers.inputText(commands)
    input_time = time.time()
    print('ELAPSED:')
    print('OCR time', (ocr_time - start_time))
    print('Input time', (input_time - ocr_time))
    print('Total', (time.time() - start_time))
    return
