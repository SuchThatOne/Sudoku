from utils import *
import copy
import csv
import time

def solve(grid):

    values = grid_values(grid)
    values = search(values)
    display(values)
    return values

if __name__ == '__main__':
    counter = 0
    correct = 0
    node_counter = 0
    #csv_reader = csv.reader(open('sudoku.csv', 'r'))
    csv_reader = csv.reader(open('sudoku_hard.csv', 'r'))
    for row in csv_reader:
        grid = row[0]
        values = solve(grid)
        counter += 1
        if counter <= 30000:
            continue        
        grid = row[0]
        start_time = time.time()
        values = solve(grid)
        if dict2chars(values) == row[1]:
            correct += 1
            #print('Solution Correct!')
        if counter >= 40000:
            break
        accuarcy = correct / counter
        print (accuarcy, '%d/%d'%(correct,counter))

    #grid = input('type sudoku as a long string of 81 characters with 0 as unsolved place\n')
    #solve(grid)
