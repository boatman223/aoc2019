import itertools
import collections
import os
import random

class Computer:

    RUNNING = 0
    PAUSED  = 1
    HALTED  = 2

    def __init__(self, code, pc=0, stdin=None):
        self.code = code
        self.pc = pc
        self.rbase = 0
        self.status = self.RUNNING
        self.stdin = stdin
        self.stdout = []
        self.execute()

    def send_input(self, stdin):
        self.stdin = stdin
        self.status = self.RUNNING
        self.pc -= 2
        self.execute()

    def get_output(self):
        output = self.stdout
        self.stdout = []
        return output

    def get_param_count(self, opcode):
        count = {
            '01': 3,
            '02': 3,
            '03': 1,
            '04': 1,
            '05': 2,
            '06': 2,
            '07': 3,
            '08': 3,
            '09': 1,
            '99': 0
        }
        return count[opcode]

    def opcode_handlers(self):
        handlers = {
            '01': self.op_ADD,
            '02': self.op_MUL,
            '03': self.op_INP,
            '04': self.op_OUT,
            '05': self.op_JIT,
            '06': self.op_JIF,
            '07': self.op_TLT,
            '08': self.op_TEQ,
            '09': self.op_RBO,
            '99': self.op_TRM
        }
        return handlers

    def set_param(self, param):
        if param[1] == '0': return self.code[param[0]]
        elif param[1] == '1': return param[0]
        elif param[1] == '2': return self.code[param[0]+self.rbase]

    def set_param_w(self, param):
        if param[1] == '0': return param[0]
        elif param[1] == '2': return param[0]+self.rbase

    def op_ADD(self, params):
        self.code[self.set_param_w(params[2])] = self.set_param(params[0]) + self.set_param(params[1])

    def op_MUL(self, params):
        self.code[self.set_param_w(params[2])] = self.set_param(params[0]) * self.set_param(params[1])

    def op_INP(self, params):
        if self.stdin == None:
            self.status = self.PAUSED
        else:
            self.code[self.set_param_w(params[0])] = self.stdin
            self.stdin = None

    def op_OUT(self, params):
        self.stdout.append(self.set_param(params[0]))
        #print(f'output: {self.stdout}')

    def op_JIT(self, params):
        if self.set_param(params[0]):
            self.pc = self.set_param(params[1])

    def op_JIF(self, params):
        if not self.set_param(params[0]):
            self.pc = self.set_param(params[1])

    def op_TLT(self, params):
        if self.set_param(params[0]) < self.set_param(params[1]):
            self.code[self.set_param_w(params[2])] = 1
        else:
            self.code[self.set_param_w(params[2])] = 0

    def op_TEQ(self, params):
        if self.set_param(params[0]) == self.set_param(params[1]):
            self.code[self.set_param_w(params[2])] = 1
        else:
            self.code[self.set_param_w(params[2])] = 0

    def op_RBO(self, params):
        self.rbase += self.set_param(params[0])

    def op_TRM(self, params):
        self.status = self.HALTED

    def execute(self):
        while self.status == self.RUNNING:
            opcode = f'{self.code[self.pc]:0>5}'[-2:]
            modes = f'{self.code[self.pc]:0>5}'[0:3][::-1]
            increment = self.get_param_count(opcode) + 1
            params = list(zip(self.code[self.pc+1:self.pc+increment], list(modes)))
            self.pc += increment
            self.opcode_handlers()[opcode](params)
        return

class Droid(Computer):

    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    def __init__(self, code, pc=0, stdin=None):
        super().__init__(code, pc, stdin)
        self.position = (0,0)
        self.tiles = collections.defaultdict(int)
        self.tiles[(0,0)] = 0
        self.steps = 0

    def process_response(self, move):
        movement = {
            self.NORTH: (0,1),
            self.SOUTH: (0,-1),
            self.WEST:  (-1,0),
            self.EAST:  (1,0)
        }
        response = self.get_output()[0]
        attempt = tuple(i+j for i, j in zip(movement[move], self.position))

        if response == 0:
            self.tiles[attempt] = 1
        elif response == 1:
            self.position = attempt
            self.tiles[attempt] = 0
        elif response == 2:
            self.position = attempt
            self.tiles[attempt] = 2

        # print(response, move, self.tiles)
        self.steps += 1
        return response

    def print_image(self):
        # os.system('cls')
        xvalues = [i[0] for i in self.tiles.keys()]
        yvalues = [i[1] for i in self.tiles.keys()]
        for i in reversed(range(min(yvalues), max(yvalues)+1)):
            line = ''
            for j in range(min(xvalues), max(xvalues)+1):
                if (j, i) not in self.tiles.keys(): line += '  '
                elif (j, i) == self.position: line += '@@'
                elif self.tiles[(j,i)] == 0: line += '..'
                elif self.tiles[(j,i)] == 1: line += '##'
                elif self.tiles[(j,i)] == 2: line += '[]'
            print(line)

def scan_tile():
    walls = []
    paths = []
    for i in range(1, 5):
        droid.send_input(i)
        result = droid.process_response(i)
        if result == 0:
            walls.append(i)
        elif result in (1,2):
            paths.append(i)
            droid.send_input(reversedir[i])
            droid.process_response(reversedir[i])

    return walls, paths

def is_valid_path(node, paths, last):
    paths += 3 - len(maze[node])
    for k, v in maze[node].items():
        if v[0] not in deadends[node] and k != last:
            paths += is_valid_path(k, paths, node)
    return paths

with open('input.txt','r') as fh:
    basecode = [int(i) for i in fh.read().strip('\n').split(',')]
    basecode.extend([0]*10000)

maze = {}
deadends = collections.defaultdict(list)
droid = Droid(basecode[:])
lastdir = 1
lastnode = (0,0)
nodepath = []
reversedir = {1:2, 2:1, 3:4, 4:3}
finished = False
while not finished:
    walls, paths = scan_tile()
    if len(walls) == 3:
        if maze:
            deadends[lastnode].append(nodepath[0])
            try: maze[droid.position][lastnode] = list(reversed([reversedir[i] for i in nodepath]))
            except KeyError: maze[droid.position] = {lastnode: list(reversed([reversedir[i] for i in nodepath]))}
            try: maze[lastnode][droid.position] = nodepath
            except KeyError: maze[lastnode] = {droid.position: nodepath}
            lastnode = droid.position
            lastdir = nodepath[0]
            nodepath2 = []
            for move in reversed([reversedir[i] for i in nodepath[:]]):
                droid.send_input(move)
                droid.process_response(move)
                nodepath2.append(move)
            nodepath = nodepath2[:]
            continue
        else:
            move = paths[0]

    elif len(walls) == 2:
        # droid.print_image()
        if paths[0] == lastdir: move = paths[1]
        else: move = paths[0]

    elif len(walls) == 1:
        if not maze:
            deadends[droid.position].append(lastdir)
        try: maze[droid.position][lastnode] = list(reversed([reversedir[i] for i in nodepath]))
        except KeyError: maze[droid.position] = {lastnode: list(reversed([reversedir[i] for i in nodepath]))}
        try: maze[lastnode][droid.position] = nodepath
        except KeyError: maze[lastnode] = {droid.position: nodepath}
        moves = paths[:]
        moves.remove(lastdir)
        for i in deadends[droid.position]:
            try: moves.remove(i)
            except: pass
        for i in moves:
            for j in maze[droid.position].keys():
                if maze[droid.position][j][0] == i:
                    if not is_valid_path(j, 0, droid.position): moves.remove(i)
        try:
            move = random.choice(moves)
        except:
            finished = True
        nodepath = []
        lastnode = droid.position
        found = False
        for k, v in maze[droid.position].items():
            if v[0] == move:
                found = True
                for step in v:
                    droid.send_input(step)
                    droid.process_response(step)
                    nodepath.append(step)
                    lastdir = reversedir[step]
        if found: continue

    droid.send_input(move)
    droid.process_response(move)
    lastdir = reversedir[move]
    nodepath.append(move)

droid.print_image()

for k, v in droid.tiles.items():
    if v == 2:
        end = k

nodedist = {}
def set_distance(node, lastnode, end, steps):
    for node2, path in maze[node].items():
        if node2 == lastnode: continue
        nodedist[node2] = steps + len(path)
        set_distance(node2, node, end, steps + len(path))
    return

set_distance((0,0), False, end, 0)
print(nodedist[end])