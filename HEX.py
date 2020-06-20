import subprocess
import time

import helpers

def checkSolution():
    badSolution = ['WRONG', 'URONG', 'CODE']
    screen = helpers.ocr(20, 2.1, 3.4, 2)
    response = helpers.formatOcr(screen)
    for item in response:
        if 'WRONG' in item:
            print('[HEX.py] Wrong solution! Trying low possibility')
            return False
    return True

def solve():
    helpers.inputText(['HEX'])
    start_time = time.time()
    screen = helpers.ocr(20, 3.7, 1.8, 2.2) 
    ocr_time = time.time()
    puzzle = helpers.formatOcr(screen, 'hex', 2)
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
    print('[HEX.py] SOLUTION:')
    print('[HEX.py] Best: ', solutionBest, ' Maybe: ', solutionMaybe, ' Low: ', solutionLow)
    if solutionBest:
        helpers.inputText(solutionBest)
    elif solutionMaybe:
        helpers.inputText(solutionMaybe)
        correct = checkSolution()
        if not correct:
            helpers.inputText(solutionLow)
    input_time = time.time()
    print('[HEX.py] Hex solve times:')
    print('[HEX.py] OCR time:', round((ocr_time - start_time), 4))
    print('[HEX.py] Solution time:', round((solution_time - ocr_time), 4))
    print('[HEX.py] Input time:', round((input_time - solution_time), 4))
    print('[HEX.py] Total:', round((time.time() - start_time), 4))
    return
