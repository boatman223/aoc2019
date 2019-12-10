import itertools

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
        self.stdout = None
        self.execute()

    def send_input(self, stdin):
        self.stdin = stdin
        self.status = self.RUNNING
        self.pc -= 2
        self.execute()

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

    def set_param(self, param, mode):
        if mode == '0': return self.code[param]
        elif mode == '1': return param
        elif mode == '2': return self.code[param+self.rbase]

    def set_param_w(self, param, mode):
        if mode == '0': return param
        elif mode == '2': return param+self.rbase

    def op_ADD(self, params, modes):
        self.code[self.set_param_w(params[2], modes[2])] = self.set_param(params[0], modes[0]) + self.set_param(params[1], modes[1])

    def op_MUL(self, params, modes):
        self.code[self.set_param_w(params[2], modes[2])] = self.set_param(params[0], modes[0]) * self.set_param(params[1], modes[1])

    def op_INP(self, params, modes):
        if self.stdin == None:
            self.status = self.PAUSED
        else:
            self.code[self.set_param_w(params[0], modes[0])] = self.stdin
            self.stdin = None

    def op_OUT(self, params, modes):
        self.stdout = self.set_param(params[0], modes[0])
        print(f'output: {self.stdout}')

    def op_JIT(self, params, modes):
        if self.set_param(params[0], modes[0]):
            self.pc = self.set_param(params[1], modes[1])

    def op_JIF(self, params, modes):
        if not self.set_param(params[0], modes[0]):
            self.pc = self.set_param(params[1], modes[1])

    def op_TLT(self, params, modes):
        if self.set_param(params[0], modes[0]) < self.set_param(params[1], modes[1]):
            self.code[self.set_param_w(params[2], modes[2])] = 1
        else:
            self.code[self.set_param_w(params[2], modes[2])] = 0

    def op_TEQ(self, params, modes):
        if self.set_param(params[0], modes[0]) == self.set_param(params[1], modes[1]):
            self.code[self.set_param_w(params[2], modes[2])] = 1
        else:
            self.code[self.set_param_w(params[2], modes[2])] = 0

    def op_RBO(self, params, modes):
        self.rbase += self.set_param(params[0], modes[0])

    def op_TRM(self, params, modes):
        self.status = self.HALTED

    def execute(self):
        while self.status == self.RUNNING:
            opcode = f'{self.code[self.pc]:0>5}'[-2:]
            modes = f'{self.code[self.pc]:0>5}'[0:3][::-1]
            increment = self.get_param_count(opcode) + 1
            params = self.code[self.pc+1:self.pc+increment]
            self.pc += increment
            self.opcode_handlers()[opcode](params, modes)
        return

with open('input.txt','r') as fh:
    basecode = [int(i) for i in fh.read().strip('\n').split(',')]
    basecode.extend([0]*10000)

runme = Computer(basecode, stdin=1)