import unittest
from unittest import TestCase
from csp_lib.sudoku import Sudoku
from constraint_prop import AC3, revised
from csp_lib.backtrack_util import mrv
from backtrack import backtracking_search
from csp_lib.util import first

easy1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2' \
        '.3..9..5.1.3.. '
harder1 = '4173698.5.3..........7......2.....6.....8.4......1.......6.3.7.5' \
          '..2.....1.4...... '


class Test(TestCase):
    def test_ac3(self):
        for puzzle in [easy1, harder1]:
            s = Sudoku(puzzle)  # construct a Sudoku problem
            s.display(s.infer_assignment())
            print("\n")

            AC3(s)
            s.display(s.infer_assignment())

            if s.goal_test(s.curr_domains):
                print("\nProblem was solved by AC3\n")
            else:
                print("\nProblem was not solved by AC3. Start searching ...\n")


if __name__ == '__main__':
    unittest.main()
