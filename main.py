from utils import *
import copy
import csv

def solve(grid):

    values = grid_values(grid)
    values = search(values)
    #display(values)
    return values

if __name__ == '__main__':
    counter = 0
    correct = 0
    csv_reader = csv.reader(open('sudoku.csv', 'r'))
    for row in csv_reader:
        counter += 1
        grid = row[0]
        values = solve(grid)
        #dict2chars(values)
        #print(dict2chars(values))
        #print(row[1])
        if dict2chars(values) == row[1]:
            correct += 1
            print('Solution Correct!')
        if counter >= 10000:
            break
        accuarcy = correct / counter
    print (accuarcy, '%d/%d'%(correct,counter))
    #grid = input('type sudoku as a long string of 81 characters with 0 as unsolved place\n')
    #solve(grid)
