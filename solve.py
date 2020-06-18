# System modules
import sys
import subprocess
import time
import argparse

# Custom modules
import HEX
import codes
import navigate
from helpers import inputText, ocr, formatOcr

# Parse arguments
parser = argparse.ArgumentParser(description='Automate ProgressDOS')
parser.add_argument('--syscode', default=None, metavar='XXX', help='3 digit code displayed on boot screen')
parser.add_argument('--hex', action='store_true', default=False, help='Only solve hex puzzle')
parser.add_argument('--dev', action='store_true', default=False, help='DEV: call debug functions')
args = parser.parse_args()
# Run adb devices to start daemon
subprocess.Popen(['adb', 'devices']).wait()

print('Open game')
subprocess.Popen(['am', 'start', '--activity-single-top', '-n', 'com.spookyhousestudios.progressbar95/com.ansca.corona.CoronaActivity'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

# If you want to only solve hex puzzle pass --hex param
if args.hex:
    HEX.solve()
    exit()

if args.dev:
    navigate.start(True)
    exit()
    screen = ocr()
    print('SCREEN:')
    print(screen)
    formatted = formatOcr(screen)
    print('FORMATTED:')
    print(formatted)
    exit()

start_time = time.time()
# Change terminal color to F0 for better OCR
inputText(['COLOR F0'])

# Get color code from upper right corner and enter it
# If player provides --syscode parameter it will be also entered
codes.enter(args.syscode)

# Explore all other directories
navigate.start()

print('ELAPSED:')
print((time.time() - start_time))
subprocess.Popen(['am', 'start', '--activity-single-top', 'com.termux/com.termux.app.TermuxActivity'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
