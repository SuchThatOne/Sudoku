import copy

rows = 'ABCDEFGHI'
cols = '123456789'

# recomment this part for 16X16 sudoku
# rows = 'ABCDEFGHIJKLMNOP'
# cols = '1234567890abcdef'

node_counter = 0

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
# Or input your special square here to square_units. 

unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def grid_values(grid):

    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
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
        uncertain = 0
        for box in values.keys():
            uncertain += len(values[box])
        uncertain -= 81
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False, 1000000
    return values, uncertain

def search(values):
    
    global node_counter
    node_counter += 1
    values, current_uncertain = reduce_puzzle(values)
    # print(current_uncertain)  # the novel heuristic
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        print(node_counter)
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
    string = ''
    for s in rows:
        for t in cols:
            string += values[s+t]
    return string