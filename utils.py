import copy

rows = 'ABCDEFGHI'
cols = '123456789'

#For pygame visualizations
assignments = []
def assign_value(values, box, value):
    """
    function to update values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values
#End pygame visualization

def display(values):

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def grid_values(grid):

    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '0':
            chars.append(digits)
    #print(len(chars))
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def eliminate(values):

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def naked_twins(values):

    twins = [box for box in values.keys() if len(values[box]) == 2]
    naked_twin = []
    for box in twins:
        digit = values[box]
        for peer in peers[box]:
            if digit==values[peer] and peer != box:
                naked_twin.append((box,peer))

    if len(naked_twin) == 0:
        return values

    for m,n in naked_twin:
        if len(values[m]) != 2:
            return values
            
        first_digit = values[m][0]
        second_digit = values[m][1]

        # Row wise elimination
        if m[0]==n[0]:
            for row in row_units:
                if m in row:
                    for element in row:
                        if first_digit in values[element] and m != element and n != element:
                            values[element] = values[element].replace(first_digit,'')
                        if second_digit in values[element] and m != element and n != element:
                            values[element] = values[element].replace(second_digit,'')


        # Column wise elimination
        if m[1]==n[1]:
            for column in column_units:
                if m in column:
                    for element in column:
                        if first_digit in values[element] and m != element and n != element:
                            values[element] = values[element].replace(first_digit,'')
                        if second_digit in values[element] and m != element and n != element:
                            values[element] = values[element].replace(second_digit,'')

        # Square wise elimination
        for square in square_units:
            if m in square and n in square:
                for element in square:
                    if first_digit in values[element] and m != element and n!= element:
                        values[element] = values[element].replace(first_digit,'')
                    if second_digit in values[element] and m != element and n!= element:
                        values[element] = values[element].replace(second_digit,'')
    return values

def reduce_puzzle(values):

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):

    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values

    square = 'To find'
    possibilities = {}
    for box in boxes:
        possibilities[box] = len(values[box])

    for i in range(2,10):
        found = 0
        for key in possibilities:
            if (possibilities[key]==i):
                square = key
                found = 1
                break
        if found == 1 :
            break

    sudokus = []
    for j in range(len(values[square])):
        dict2 = copy.deepcopy(values)
        sudokus.append(dict2)

    count = 0

    for digit in values[square]:
        sudokus[count][square] = digit
        assign_value(values, square, digit)
        count = count + 1

    for sudoku in sudokus:
        new_sudoku = copy.deepcopy(sudoku)
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def dict2chars(values):
    
    string = values['A1'] + values['A2'] + values['A3'] + values['A4'] + values['A5'] + values['A6'] + values['A7'] + values['A8'] + values['A9'] + values['B1'] + values['B2'] + values['B3'] + values['B4'] + values['B5'] + values['B6'] + values['B7'] + values['B8'] + values['B9'] + values['C1'] + values['C2'] + values['C3'] + values['C4'] + values['C5'] + values['C6'] + values['C7'] + values['C8'] + values['C9'] + values['D1'] + values['D2'] + values['D3'] + values['D4'] + values['D5'] + values['D6'] + values['D7'] + values['D8'] + values['D9'] + values['E1'] + values['E2'] + values['E3'] + values['E4'] + values['E5'] + values['E6'] + values['E7'] + values['E8'] + values['E9'] + values['F1'] + values['F2'] + values['F3'] + values['F4'] + values['F5'] + values['F6'] + values['F7'] + values['F8'] + values['F9'] + values['G1'] + values['G2'] + values['G3'] + values['G4'] + values['G5'] + values['G6'] + values['G7'] + values['G8'] + values['G9'] + values['H1'] + values['H2'] + values['H3'] + values['H4'] + values['H5'] + values['H6'] + values['H7'] + values['H8'] + values['H9'] + values['I1'] + values['I2'] + values['I3'] + values['I4'] + values['I5'] + values['I6'] + values['I7'] + values['I8'] + values['I9']
    return string