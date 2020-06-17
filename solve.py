# System modules
import sys
import subprocess
import time

# Custom modules
import HEX
import codes

# Run adb devices to start daemon
subprocess.Popen(['adb', 'devices'], stdout=subprocess.DEVNULL).wait()

print('Open game')
subprocess.Popen(['am', 'start', '--activity-single-top', '-n', 'com.spookyhousestudios.progressbar95/com.ansca.corona.CoronaActivity'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

# If you want to only solve hex puzzle pass --hex param
if sys.argv[1] == '--hex':
    HEX.solve()
    exit()

start_time = time.time()
# Change terminal color to F0 for better OCR
subprocess.Popen(['adb', 'shell', 'input', 'text', 'F0']).wait()
subprocess.Popen(['adb', 'shell', 'input', 'keyevent', '66'])

# Get color code from upper right corner and enter it
# If player provides syscode as first parameter it will be also entered
# codes.enter(sys.argv[1])
# TODO

# Explore all other directories

print('ELAPSED:')
print((time.time() - start_time))
subprocess.Popen(['am', 'start', '--activity-single-top', 'com.termux/com.termux.app.TermuxActivity'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
