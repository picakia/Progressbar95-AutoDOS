import subprocess
import time

import helpers

def solve():
    helpers.inputText(['HEX'])
    start_time = time.time()
    screen = helpers.ocr(20, 3.7, 1.8, 2.2) 
    ocr_time = time.time()
    unformattedPuzzle = screen.split(' ')
    print('Before format:')
    print(unformattedPuzzle)
    puzzle = helpers.formatOcr(screen, True, True, 3)
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
        helpers.inputText(solutionBest)
    elif solutionMaybe:
        helpers.inputText(solutionMaybe)
    input_time = time.time()
    print('ELAPSED:')
    print('OCR time', (ocr_time - screen_time))
    print('Solution time', (solution_time - ocr_time))
    print('Input time', (input_time - solution_time))
    print('Total', (time.time() - start_time))
    return