import itertools
import numpy as np

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

class Painter(Computer):

    RIGHT = 90
    LEFT = -90

    BLACK = 0
    WHITE = 1

    def __init__(self, code, pc=0, stdin=None):
        super().__init__(code, pc, stdin)
        self.facing = 0
        self.position = np.array([0,0])
        self.tiles = {}

    def process_orders(self, data):
        orders = []
        if data[0] == 0: orders.append(self.BLACK)
        elif data[0] == 1: orders.append(self.WHITE)
        if data[1] == 0: orders.append(self.LEFT)
        elif data[1] == 1: orders.append(self.RIGHT)
        orders.append(1)

        self.turn(orders)
        for _ in range(orders[2]):
            self.paint(orders)
            self.move()

    def turn(self, orders):
        self.facing = (self.facing + orders[1]) % 360

    def paint(self, orders):
        self.tiles[tuple(self.position)] = orders[0]

    def move(self):
        movement = {
            0:   np.array([0,1]),
            90:  np.array([1,0]),
            180: np.array([0,-1]),
            270: np.array([-1,0])
        }
        self.position += movement[self.facing]


with open('input.txt','r') as fh:
    basecode = [int(i) for i in fh.read().strip('\n').split(',')]
    basecode.extend([0]*10000)

painter = Painter(basecode[:], stdin=0)
while painter.status != painter.HALTED:
    orders = painter.get_output()
    painter.process_orders(orders)
    try:
        painter.send_input(painter.tiles[tuple(painter.position)])
    except KeyError:
        painter.send_input(0)

print(painter.tiles)
print(len(painter.tiles))