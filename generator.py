import numpy as np
import random
from math import sqrt

neighborhood = [(1,0),(-1,0),(0,1),(0,-1)]

def valid_coordinate(n, x, y):
    return x>=0 and x<n and y>=0 and y<n

def visualize_blocks(n, block_list):
    label_map = np.zeros([n,n])
    for i, block in enumerate(block_list):
        for x,y in block:
            label_map[x,y] = i+1
    print(label_map)

def random_partition(n):
    used = np.zeros([n, n], np.bool)
    block_list = []

    def check():
        used_true = np.zeros([n, n], np.bool)
        for block in block_list:
            for x,y in block:
                assert(used_true[x,y] == False)
                used_true[x,y] = True
        assert(np.array_equal(used, used_true))

    def put_block(x, y, remain, block):
        if used[x, y]:
            return False
        used[x, y] = True
        block.append((x,y))
        if remain == 0:
            return True
        randomized_neighborhood = random.sample(neighborhood, len(neighborhood))
        for delta in randomized_neighborhood:
            x1 = x + delta[0]
            y1 = y + delta[1]
            if not valid_coordinate(n, x1, y1):
                continue
            res = put_block(x1, y1, remain-1, block)
            if res == True:
                return True
        used[x, y] = False
        block.pop()
        return False

    def remove_block():
        last_block = block_list.pop()
        for x, y in last_block:
            used[x, y] = False

    while len(block_list) < n:
        var_x, var_y = -1, -1
        for i in range(n):
            for j in range(n):
                if not used[i, j]:
                    var_x, var_y = i, j
                    break
            if var_x >= 0:
                break
        new_block = []
        res = put_block(var_x, var_y, n-1, new_block)
        if res:
            block_list.append(new_block)
            # visualize_blocks(n, block_list)
        else:
            while random.random() < 0.5 and len(block_list) > 0:
                remove_block()
    return block_list

def normal_partition(n):
    block_list = []
    m = int(sqrt(n))
    if m*m != n:
        raise ValueError("n should be a square number!")
    for i in range(m):
        for j in range(m):
            new_block = []
            for x in range(m):
                for y in range(m):
                    new_block.append((i*m+x, j*m+y))
            block_list.append(new_block)
    return block_list

def generate_puzzle(n, partition_function=random_partition):
    block_list = partition_function(n)
    label_map = np.zeros([n,n], np.int)
    for i, block in enumerate(block_list):
        for x,y in block:
            label_map[x,y] = i
    sol = np.zeros([n,n], np.int)

    def check(x,y):
        for i in range(x):
            if sol[x,y] == sol[i,y]:
                return False
        for j in range(y):
            if sol[x,y] == sol[x,j]:
                return False
        for i,j in block_list[label_map[x,y]]:
            if (i<x or i==x and j<y) and sol[x,y] == sol[i,j]:
                return False
        return True

    def trivial_search(x, y):
        if x >= n:
            return True
        for v in random.sample(range(n),n):
            sol[x, y] = v
            if check(x,y):
                if y == n-1:
                    res = trivial_search(x+1, 0)
                else:
                    res = trivial_search(x, y+1)
                if res:
                    return True
        return False

    if not trivial_search(0,0):
        return None
    return label_map, sol

if __name__ == '__main__':
    label_map, sol = generate_puzzle(7)
    print("partition label map:\n", label_map)
    print("one solution:\n", sol)