from csp_lib.sudoku import (Sudoku, easy1, harder1)
from constraint_prop import AC3
from csp_lib.backtrack_util import mrv, lcv, mac
from backtrack import backtracking_search

for puzzle in [easy1, harder1]:
    sudoku_instance = Sudoku(puzzle)

    print("We have the following Sudoku puzzle to solve:", end="\n\n")
    sudoku_instance.display(sudoku_instance.infer_assignment())
    print("\nStarting constraint propagation (AC3) algorithm.")
    AC3(sudoku_instance)
    print("AC3 algorithm was successfully completed.")

    if sudoku_instance.goal_test(sudoku_instance.curr_domains):
        print("Problem was solved by AC3. Here is the solution:", end="\n\n")
        sudoku_instance.display(sudoku_instance.infer_assignment())
        print()
    else:
        print("Problem was not solved by AC3. Here is how it looks like:",
              end="\n\n")
        sudoku_instance.display(sudoku_instance.infer_assignment())
        print()
        print("We should start searching ...")
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
