import subprocess
import time

# Custom modules
import helpers

def enter(program):
    start_time = time.time()
    commands = []
    if program == 'COLORCODE':
        # Get color code from upper right corner and enter it when found
        screen = helpers.ocr(1.16, 4.6, 1.07, 4.1)
        colorcode = helpers.formatOcr(screen, 'hex', 2)
        if colorcode:
            commands.extend([program, colorcode[0]]);
    if program == 'SYSCODE':
        if not syscode:
            return
        # Input code syscode
        commands.extend([program, syscode]);
    if program == 'CODEX':
        if not codex:
            return
        # Input Lorem code
        commands.extend([program, syscode]);

    helpers.inputText(commands)
    print('CODES ELAPSED:\n', round((time.time() - start_time), 4))
    return
