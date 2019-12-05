import collections

def draw_right(grid, steps, length, currentpos, currentsize, wirenum):

    def extend_right(grid, extend, currentsize):
        currentsize['x'] += extend
        for row in grid:
            row.extend([0]*extend)
        return grid, currentsize

    if length > (currentsize['x'] - currentpos['x']):
        extend = length - (currentsize['x'] - currentpos['x'])
        grid, currentsize = extend_right(grid, extend, currentsize)
    for i in range(currentpos['x'], currentpos['x'] + length):
        steps += 1
        if wirenum == 1:
            if grid[currentpos['y']][i+1] == 0:
                grid[currentpos['y']][i+1] = steps
        elif wirenum == 2:
            if grid[currentpos['y']][i+1] != 0:
                oldsteps = grid[currentpos['y']][i+1]
                totalsteps = oldsteps + steps
                print(f'intersection found - {totalsteps} steps - {oldsteps} {steps}')
    currentpos['x'] += length
    return grid, steps, currentpos, currentsize

def draw_up(grid, steps, length, currentpos, currentsize, wirenum):
    
    def extend_up(grid, extend, currentsize):
        currentsize['y'] += extend
        for i in range(extend):
            grid.append(collections.deque([0]*(currentsize['x']+1)))
        return grid, currentsize

    if length > (currentsize['y'] - currentpos['y']):
        extend = length - (currentsize['y'] - currentpos['y'])
        grid, currentsize = extend_up(grid, extend, currentsize)
    for i in range(currentpos['y'], currentpos['y'] + length):
        steps += 1
        if wirenum == 1:
            if grid[i+1][currentpos['x']] == 0:
                grid[i+1][currentpos['x']] = steps
        elif wirenum == 2:
            if grid[i+1][currentpos['x']] != 0:
                oldsteps = grid[i+1][currentpos['x']]
                totalsteps = oldsteps + steps
                print(f'intersection found - {totalsteps} steps - {oldsteps} {steps}')
    currentpos['y'] += length
    return grid, steps, currentpos, currentsize  

def draw_left(grid, steps, length, startpos, currentpos, currentsize, wirenum):

    def extend_left(grid, extend, startpos, currentpos, currentsize):
        startpos['x'] += extend
        currentpos['x'] += extend
        currentsize['x'] += extend
        for row in grid:
            row.extendleft([0]*extend)
        return grid, startpos, currentpos, currentsize

    if length > currentpos['x']:
        extend = length - currentpos['x']
        grid, startpos, currentpos, currentsize = extend_left(grid, extend, startpos, currentpos, currentsize)
    for i in reversed(range(currentpos['x'] - length, currentpos['x'])):
        steps += 1
        if wirenum == 1:
            if grid[currentpos['y']][i] == 0:
                grid[currentpos['y']][i] = steps
        elif wirenum == 2:
            if grid[currentpos['y']][i] != 0:
                oldsteps = grid[currentpos['y']][i]
                totalsteps = oldsteps + steps
                print(f'intersection found - {totalsteps} steps - {oldsteps} {steps}')

    currentpos['x'] -= length
    return grid, steps, startpos, currentpos, currentsize

def draw_down(grid, steps, length, startpos, currentpos, currentsize, wirenum):

    def extend_down(grid, extend, startpos, currentpos, currentsize):
        startpos['y'] += extend
        currentpos['y'] += extend
        currentsize['y'] += extend
        for i in range(extend):
            grid.appendleft(collections.deque([0]*(currentsize['x']+1)))
        return grid, startpos, currentpos, currentsize

    if length > currentpos['y']:
        extend = length - currentpos['y']
        grid, startpos, currentpos, currentsize = extend_down(grid, extend, startpos, currentpos, currentsize)
    for i in reversed(range(currentpos['y'] - length, currentpos['y'])):
        steps += 1
        if wirenum == 1:
            if grid[i][currentpos['x']] == 0:
                grid[i][currentpos['x']] = steps
        if wirenum == 2:
            if grid[i][currentpos['x']] != 0:
                oldsteps = grid[i][currentpos['x']]
                totalsteps = oldsteps + steps
                print(f'intersection found - {totalsteps} steps - {oldsteps} {steps}')
    currentpos['y'] -= length
    return grid, steps, startpos, currentpos, currentsize

def draw_wire(grid, wire, startpos, currentpos, currentsize, wirenum):
    steps = 0
    for segment in wire:
        direction = segment[0]
        length = int(segment[1:])
        if direction == 'R':
            grid, steps, currentpos, currentsize = draw_right(grid, steps, length, currentpos, currentsize, wirenum)
        elif direction == 'U':
            grid, steps, currentpos, currentsize = draw_up(grid, steps, length, currentpos, currentsize, wirenum)
        elif direction == 'L':
            grid, steps, startpos, currentpos, currentsize = draw_left(grid, steps, length, startpos, currentpos, currentsize, wirenum)
        elif direction == 'D':
            grid, steps, startpos, currentpos, currentsize = draw_down(grid, steps, length, startpos, currentpos, currentsize, wirenum)

    return grid, startpos, currentpos, currentsize

def print_grid(grid, startpos):
    with open('output.txt', 'w') as outputfile:
        #print('\n')
        # i = len(grid)
        for row in reversed(grid):
            # i -= 1
            output = ''
            for j, column in enumerate(row):
                # if (i, j) == (startpos['y'], startpos['x']):
                #     output += 'X'
                # else:
                #     output += str(column) 
                output += str(column)
            #print(output)
            outputfile.write(output+'\n')

grid = collections.deque([collections.deque([0])])
with open('input.txt', 'r') as fh:
    wirenum = 1
    startpos = {'x': 0, 'y': 0}
    currentpos = {'x': 0, 'y': 0}
    currentsize = {'x': 0, 'y': 0}
    while wirenum < 3:
        wire = fh.readline().split(',')
        print(wire)
        grid, startpos, currentpos, currentsize = draw_wire(grid, wire, startpos, currentpos, currentsize, wirenum)
        currentpos['x'] = startpos['x']
        currentpos['y'] = startpos['y']
        # print_grid(grid, startpos)
        wirenum += 1

    