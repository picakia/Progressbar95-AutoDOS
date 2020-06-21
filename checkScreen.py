from PIL import Image
import subprocess
import time

resolution = subprocess.run(['adb', 'shell', 'wm', 'size'], universal_newlines=True, stdout=subprocess.PIPE)
width, height = resolution.stdout[15:-1].split('x')
width = int(width)
height = int(height)
print('Your resolution:', width, height)

subprocess.Popen(['am', 'start', '--activity-single-top', '-n', 'com.spookyhousestudios.progressbar95/com.ansca.corona.CoronaActivity'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

start = time.time()
screenShot = subprocess.Popen(['adb', 'shell', 'screencap', '/sdcard/dos.raw']).wait()
screen = time.time()
file = open('/sdcard/dos.raw', 'rb')
raw = file.read()
file.close()
game = Image.frombuffer('RGBA', (width,height), raw, 'raw', 'RGBA', 0, 1)
imOpen = time.time()
crop = (round(width/20), round(height/4.7), round(width/1.05), round(height/2))
dos = game.crop(crop)
crop = time.time()
dos.save('/sdcard/vision.png', 'PNG')
dos.save('/sdcard/vision.ppm', 'PPM')
save = time.time()
ocrad = subprocess.run(["ocrad", "--scale=2", "/sdcard/vision.ppm"], universal_newlines=True, errors='replace', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
vision = ocrad.stdout
ocr = time.time()
print('Vision:\n', vision)
print('Times:')
print('Screenshot time:\n', screen-start)
print('Image open time:\n', imOpen-screen)
print('Crop time:\n', crop-imOpen)
print('Save time:\n', save-crop)
print('OCR time:\n', ocr-save)
print('Overall time:\n', ocr-start)

subprocess.Popen(['am', 'start', '--activity-single-top', 'com.termux/com.termux.app.TermuxActivity'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
