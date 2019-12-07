import itertools

def get_parameter_count(opcode):
    count = {
        '01': 3,
        '02': 3,
        '03': 1,
        '04': 1,
        '05': 2,
        '06': 2,
        '07': 3,
        '08': 3,
        '99': 0
    }
    return count[opcode]

def opcode_handlers():
    handlers = {
        '01': op_ADD,
        '02': op_MUL,
        '03': op_INP,
        '04': op_OUT,
        '05': op_JIT,
        '06': op_JIF,
        '07': op_TLT,
        '08': op_TEQ,
        '99': op_TRM
    }
    return handlers

def set_parameter(code, parameter, mode):
    if mode == '0': return code[parameter]
    elif mode == '1': return parameter

def op_ADD(code, index, parameters, phase, inputval):
    code[code[index-1]] = parameters[0] + parameters[1]
    return code, index, phase, 0

def op_MUL(code, index, parameters, phase, inputval):
    code[code[index-1]] = parameters[0] * parameters[1]
    return code, index, phase, 0

def op_INP(code, index, parameters, phase, inputval):
    if phase != 999:
        code[code[index-1]] = phase
        phase = 999
    else:
        code[code[index-1]] = inputval
    return code, index, phase, 0

def op_OUT(code, index, parameters, phase, inputval):
    phase = parameters[0]
    print(f'output: {parameters[0]}')
    return code, index, phase, 1

def op_JIT(code, index, parameters, phase, inputval):
    if parameters[0]: index = parameters[1]
    return code, index, phase, 0

def op_JIF(code, index, parameters, phase, inputval):
    if not parameters[0]: index = parameters[1]
    return code, index, phase, 0

def op_TLT(code, index, parameters, phase, inputval):
    if parameters[0] < parameters[1]: code[code[index-1]] = 1
    else: code[code[index-1]] = 0
    return code, index, phase, 0

def op_TEQ(code, index, parameters, phase, inputval):
    if parameters[0] == parameters[1]: code[code[index-1]] = 1
    else: code[code[index-1]] = 0
    return code, index, phase, 0

def op_TRM(code, index, parameters, phase, inputval):
    return code, index, phase, 2

def run_computer(code, phase, inputval):
    done = 0
    index = 0
    while not done:
        opcode = f'{code[index]:0>5}'[-2:]
        modes = f'{code[index]:0>5}'[0:3][::-1]
        increment = get_parameter_count(opcode) + 1
        parameters = code[index+1:index+increment]
        index += increment
        for i, parameter in enumerate(parameters[:]):
            mode = modes[i]
            parameters[i] = set_parameter(code, parameter, mode)
        code, index, phase, done = opcode_handlers()[opcode](code, index, parameters, phase, inputval)
    return phase

with open('input.txt','r') as fh:
    basecode = [int(i) for i in fh.read().strip('\n').split(',')]

tests = list(itertools.permutations([0,1,2,3,4]))

highest_output = 0
for test in tests:
    output = 0
    for i in range(0,5):
        output = run_computer(basecode[:], test[i], output)
    if output > highest_output:
        highest_output = output

print(highest_output)