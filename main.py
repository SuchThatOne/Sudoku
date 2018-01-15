from utils import *
import copy
import csv
import time

def solve(grid):

    values = grid_values(grid)
    values = search(values)
    display(values) # whether display your solution
    return values

if __name__ == '__main__':
    # counter = 0 # re-comment to select heuristic 
    # correct = 0
    node_counter = 0
    # csv_reader = csv.reader(open('sudoku.csv', 'r')) # this dataset is over 100MB and used to adjust the heuristic to select.
    csv_reader = csv.reader(open('sudoku_hard.csv', 'r')) # the test set
    for row in csv_reader:
        grid = row[0]
        values = solve(grid)
        #counter += 1
        ''' 
        # this part is along with the 'sudoku.csv'
        if counter <= 350000:
            continue        
        grid = row[0]
        start_time = time.time()
        values = solve(grid)
        if dict2chars(values) == row[1]:
            correct += 1
            print('Solution Correct!')
        if counter >= 400000:
            break
        accuarcy = correct / counter
        print (accuarcy, '%d/%d'%(correct,counter))
        '''
    # grid = input('type sudoku as a long string of 81 characters with 0 as unsolved place\n') # re-comment this 2 line to use it as a input mode
    # solve(grid)
