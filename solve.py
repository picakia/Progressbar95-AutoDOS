# System modules
import sys
import subprocess
import time
import argparse

# Run adb devices to start daemon first
adbOut = subprocess.run(['adb','devices'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
devCheck = adbOut.stdout.replace('\t', '\n').split('\n')
if 'device' not in devCheck:
    print('No ADB device found! Check Readme on github page for possible solutions!')
    exit()

# Load custom modules
import HEX
import codes
import navigate
from helpers import inputText, ocr, formatOcr

# Parse arguments
parser = argparse.ArgumentParser(description='Automate ProgressDOS')
parser.add_argument('-s, --syscode', default=None, metavar='XXX', help='3 digit code displayed on boot screen', dest='syscode')
parser.add_argument('-h, --hex', action='store_true', default=False, help='Only solve hex puzzle', dest='hex')
parser.add_argument('-d, --dir', action='store_true', default=0, help='Browse from current directory', dest='dir')
parser.add_argument('-l, --level', metavar='level', type=int, default=0, help='Starting directory level for --dir option', dest='level')
parser.add_argument('--dev', action='store_true', default=False, help='DEV: call debug functions')
args = parser.parse_args()

codes.syscode = args.syscode

print('Open game')
subprocess.Popen(['am', 'start', '--activity-single-top', '-n', 'com.spookyhousestudios.progressbar95/com.ansca.corona.CoronaActivity'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

# If you want to only solve hex puzzle pass --hex param
if args.hex:
    HEX.solve()
    exit()

# If you want to browse from current dir pass --dir param
if args.dir:
    navigate.start(True, args.level)
    exit()

if args.dev:
    screen = ocr(20, 4.7, 1.05, 2)
    print('SCREEN:')
    print(screen)
    formatted = formatOcr(screen)
    print('FORMATTED:')
    print(formatted)
    exit()

start_time = time.time()
# Change terminal color to F0 for better OCR
inputText(['COLOR F0'])

# Explore all other directories
navigate.start()

print('ELAPSED:')
print((time.time() - start_time))
subprocess.Popen(['am', 'start', '--activity-single-top', 'com.termux/com.termux.app.TermuxActivity'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
