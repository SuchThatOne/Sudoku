from utils import *
import copy

def solve(grid):

    values = grid_values(grid)
    values = search(values)
    display(values)

if __name__ == '__main__':
    grid = input('type sudoku as a long string of 81 characters with 0 as unsolved place\n')
    solve(grid)
