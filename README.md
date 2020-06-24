# Progressbar95-AutoDOS
Automation for ProgressDOS/ProgressCMD/ProgressShell in Progressbar95 game

## Features
* Runs directly from your device, no computer needed when solving!
* Goes through every folder
* Auto detects HEX puzzles and solves them
* Optimized for best score possible
* Enters COLORCODE (and SYSCODE when provided)
* Can run from current folder (**remember to set COLOR F0 in ProgressDOS**)
* Can only solve HEX puzzles if you don't want more help
* Written fully in Termux and Vim on my android phone (c'mon isn't that a feature?)

## Requirements
* Termux
* git
* Python 3
* Pillow image engine
* ocrad OCR engine
* ADB for Termux
* libjpg-turbo
* Keyboard without autocompletion

## Installation:
1. Install keyboard without autocompletion and set it as input method while running script (this is because autocompletion messes with input, I'm using Hacker's keyboard)
2. Install and Open Termux
3. `apt update && apt install git python ocrad libjpg-turbo && pip install Pillow`
4. Install Termux adb tools from [HERE](https://github.com/MasterDevX/Termux-ADB)
5. `git clone https://github.com/picakia/Progressbar95-AutoDOS.git`

## Basic usage
1. Make sure you have all of above installed
2. Enable USB debugging (in Settings->Developer options)
3. If you don't have root:
   * Connect phone with USB cable to computer
   * Open cmd where you have adb installed (Minimal ADB and fasboot recommended - [LINK](https://forum.xda-developers.com/showthread.php?t=2317790))
   * Check if your device shows using `adb devices`
   * If you don't see your device look for adb tutorial in google
   * Run `adb tcpip 5555`
   * Disconnect phone
4. Open Progressbar95 and ProgressDOS window
5. Open Termux and cd into AutoDOS directory (`cd Progressbar95-AutoDOS`)
6. Run `python solve.py`

## Advanced usage
```
python solve.py [-h] [-s, --syscode XXX] [-h, --hex] [-d, --dir] [-l, --level level] [--dev]
optional arguments:
  -h, --help         show this help message and exit
  -s, --syscode XXX  3 digit code displayed on Progressbar boot screen
  -h, --hex          Only solve hex puzzle
  -d, --dir          Browse from current directory
  -l, --level level  Starting directory level for --dir option
  --dev              DEV: call debug functions
```
## Notes
* Eploring can take anywhere from 20 to 70 minutes depending on folders generated
* After exploring is done you need to play at least one normal game to collect points
* If you need to stop executing script just lock your screen for few moments or switch to Termux and hit CTRL+C

## Credits
Many thanks to:
* [Samuel Rodberg](https://github.com/samrodberg) for Minimal ADB and fastboot package
* [MasterDevX](https://github.com/MasterDevX) for ADB Termux tools
* [Termux team](https://github.com/termux) for Termux
* [Pillow team](https://github.com/python-pillow) for Pillow image engine
And everyone else for providing tools to make this project possible. Thank you all! ❤︎ 
