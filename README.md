# Progressbar95-AutoDOS
Automation for ProgressDOS in Progressbar95 game on your android device

## Requirements
* Termux
* Python 3
* ocrad OCR engine
* ADB for Termux
* libjpg-turbo

## Installation:
1. Open Termux
2. Install all of above
3. Clone into directory

## Basic usage
1. Make sure you have all of above installed
2. Enable USB debbuging
3. If you don't have root:
   * Connect phone with usb to computer
   * Open cmd where you have adb installed (Minimal ADB and fasboot recommended - google it)
   * Check if your device shows ```adb devices```
   * Run ```adb tcpip 555```
   * Disconnect phone
4. Open Progressbar95 and ProgressDOS window
5. Open Termux and cd into AutoDOS directory
6. ```python solve.py```

**For advanced usage run ```python solve.py -h```**
