from csp_lib.sudoku import (Sudoku, easy1, harder1)
from constraint_prop import AC3
from csp_lib.backtrack_util import mrv, lcv, mac
from backtrack import backtracking_search

for puzzle in [easy1, harder1]:
    sudoku_instance = Sudoku(puzzle)  # construct a Sudoku problem

    sudoku_instance.display(sudoku_instance.infer_assignment())
    print("\n")

    AC3(sudoku_instance)
    sudoku_instance.display(sudoku_instance.infer_assignment())
    print(sudoku_instance.curr_domains)

    if sudoku_instance.goal_test(sudoku_instance.curr_domains):
        print("\nProblem was solved by AC3\n")
    else:
        print("\nProblem was not solved by AC3. Start searching ...\n")
        search_result = backtracking_search(sudoku_instance, mrv, lcv, mac)
        print("Search has been completed successfully.")
        if sudoku_instance.goal_test(search_result):
            print("Given constraint satisfaction problem has been "
                  "successfully solved by backtracking search algorithm. Here "
                  "it the solution:", end='\n\n')
            sudoku_instance.display(sudoku_instance.infer_assignment())
        else:
            print("Backtracking search algorithm was not able to solve the "
                  "problem.", end='\n\n')
            sudoku_instance.display(sudoku_instance.infer_assignment())

    correct_assignment = {0: ['4'], 1: ['8'], 2: ['3'], 9: ['9'], 10: ['2'],
                          11: ['1'], 18: ['6'], 19: ['5'], 20: ['7'], 3: ['9'],
                          4: ['6'], 5: ['7'], 12: ['3'], 13: ['4'], 14: ['5'],
                          21: ['8'], 22: ['2'], 23: ['1'], 6: ['2'], 7: ['5'],
                          8: ['1'], 15: ['8'], 16: ['7'], 17: ['6'], 24: ['4'],
                          25: ['9'], 26: ['3'], 27: ['5'], 28: ['4'], 29: ['8'],
                          36: ['1'], 37: ['3'], 38: ['2'], 45: ['9'], 46: ['7'],
                          47: ['6'], 30: ['7'], 31: ['2'], 32: ['9'], 39: ['5'],
                          40: ['6'], 41: ['4'], 48: ['1'], 49: ['3'], 50: ['8'],
                          33: ['1'], 34: ['3'], 35: ['6'], 42: ['7'], 43: ['9'],
                          44: ['8'], 51: ['2'], 52: ['4'], 53: ['5'], 54: ['3'],
                          55: ['7'], 56: ['2'], 63: ['6'], 64: ['8'], 65: ['9'],
                          72: ['5'], 73: ['1'], 74: ['4'], 57: ['8'], 58: ['1'],
                          59: ['4'], 66: ['2'], 67: ['5'], 68: ['3'], 75: ['7'],
                          76: ['6'], 77: ['9'], 60: ['6'], 61: ['9'], 62: ['5'],
                          69: ['4'], 70: ['1'], 71: ['7'], 78: ['3'], 79: ['8'],
                          80: ['2']}
