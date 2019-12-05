import collections

def draw_right(grid, length, currentpos, currentsize, wirenum):

    def extend_right(grid, extend, currentsize):
        currentsize['x'] += extend
        for row in grid:
            row.extend([0]*extend)
        return grid, currentsize

    if length > (currentsize['x'] - currentpos['x']):
        extend = length - (currentsize['x'] - currentpos['x'])
        grid, currentsize = extend_right(grid, extend, currentsize)
    for i in range(currentpos['x'], currentpos['x'] + length):
        grid[currentpos['y']][i+1] += wirenum
    currentpos['x'] += length
    return grid, currentpos, currentsize

def draw_up(grid, length, currentpos, currentsize, wirenum):
    
    def extend_up(grid, extend, currentsize):
        currentsize['y'] += extend
        for i in range(extend):
            grid.append(collections.deque([0]*(currentsize['x']+1)))
        return grid, currentsize

    if length > (currentsize['y'] - currentpos['y']):
        extend = length - (currentsize['y'] - currentpos['y'])
        grid, currentsize = extend_up(grid, extend, currentsize)
    for i in range(currentpos['y'], currentpos['y'] + length):
        grid[i+1][currentpos['x']] += wirenum
    currentpos['y'] += length
    return grid, currentpos, currentsize  

def draw_left(grid, length, startpos, currentpos, currentsize, wirenum):

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
    for i in range(currentpos['x'] - length, currentpos['x']):
        grid[currentpos['y']][i] += wirenum
    currentpos['x'] -= length
    return grid, startpos, currentpos, currentsize

def draw_down(grid, length, startpos, currentpos, currentsize, wirenum):

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
    for i in range(currentpos['y'] - length, currentpos['y']):
        grid[i][currentpos['x']] += wirenum
    currentpos['y'] -= length
    return grid, startpos, currentpos, currentsize

def draw_wire(grid, wire, startpos, currentpos, currentsize, wirenum):
    for segment in wire:
        direction = segment[0]
        length = int(segment[1:])
        if direction == 'R':
            grid, currentpos, currentsize = draw_right(grid, length, currentpos, currentsize, wirenum)
        elif direction == 'U':
            grid, currentpos, currentsize = draw_up(grid, length, currentpos, currentsize, wirenum)
        elif direction == 'L':
            grid, startpos, currentpos, currentsize = draw_left(grid, length, startpos, currentpos, currentsize, wirenum)
        elif direction == 'D':
            grid, startpos, currentpos, currentsize = draw_down(grid, length, startpos, currentpos, currentsize, wirenum)

        print(currentsize)
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
    while True:
        wire = fh.readline().split(',')
        print(wire)
        if wire == ['']: break
        grid, startpos, currentpos, currentsize = draw_wire(grid, wire, startpos, currentpos, currentsize, wirenum)
        currentpos['x'] = startpos['x']
        currentpos['y'] = startpos['y']
        # print_grid(grid, startpos)
        wirenum *= 10

print(startpos)
lowestdist = 9999
for i, row in enumerate(grid):
    for j, column in enumerate(row):
        if column > 10 and column % 10 > 0:
            xdist = abs(startpos['x']-j)
            ydist = abs(startpos['y']-i)
            dist = xdist+ydist
            if dist < lowestdist: lowestdist = dist
            print(f'intersection at {j},{i} - distance {dist} - lowest {lowestdist}')