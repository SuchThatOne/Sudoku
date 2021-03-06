import numpy as np
import random
from math import sqrt
import threading
import time

neighborhood = [(1,0),(-1,0),(0,1),(0,-1)]

def valid_coordinate(n, x, y):
    return x>=0 and x<n and y>=0 and y<n

def visualize_blocks(n, block_list):
    label_map = np.zeros([n,n])
    for i, block in enumerate(block_list):
        for x,y in block:
            label_map[x,y] = i+1
    print(label_map)

def random_partition(n, timeout=1e8):
    used = np.zeros([n, n], np.bool)
    block_list = []
    start_time = time.time()

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
        if time.time()-start_time > timeout:
            return None

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
            while random.random() < 0.1 and len(block_list) > 0:
                remove_block()
    return block_list

def normal_partition(n, timeout=1e8):
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

max_x, max_y = 0, 0
found = False
label_map_g, sol_g = None, None

def generate_puzzle(n, partition_function=random_partition, timeout1=1e8, timeout2=1e8):
    global found, label_map_g, sol_g

    block_list = partition_function(n, timeout=timeout1)
    if block_list == None:
        return None
    label_map = np.zeros([n,n], np.int)
    for i, block in enumerate(block_list):
        for x,y in block:
            label_map[x,y] = i
    sol = np.zeros([n,n], np.int)

    start_time = time.time()
    # print(label_map)

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
        global max_x, max_y
        if found or time.time()-start_time > timeout2:
            return False
        if x > max_x or x == max_x and y > max_y:
            max_x, max_y = x, y
            # print(max_x, max_y)
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

    label_map_g = label_map
    sol_g = sol
    found = True
    return label_map, sol

def quick_random_generate(n):
    threads = []
    global label_map_g
    while label_map_g is None:
        threads.append(threading.Thread(target=generate_puzzle, args=(n,random_partition,2,4)))
        threads[-1].start()
        threads.append(threading.Thread(target=generate_puzzle, args=(n,random_partition,2,4)))
        threads[-1].start()
        threads[-2].join()
        threads[-1].join()
        # print(len(threads))

if __name__ == '__main__':
    quick_random_generate(9)
    print("partition label map:\n", label_map_g)
    print("one solution:\n", sol_g)