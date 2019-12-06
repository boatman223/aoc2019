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
    if mode == '0':
        val = code[parameter]
    elif mode == '1':
        val = parameter
    return val

def op_ADD(code, index, parameters):
    code[code[index-1]] = parameters[0] + parameters[1]
    return code, index, False

def op_MUL(code, index, parameters):
    code[code[index-1]] = parameters[0] * parameters[1]
    return code, index, False

def op_IN(code, index, parameters):
    code[code[index-1]] = inputval
    return code, index, False

def op_OUT(code, index, parameters):
    print(f'output: {parameters[0]}')
    return code, index, False

def op_JIT(code, index, parameters):
    if parameters[0]: index = parameters[1]
    return code, index, False

def op_JIF(code, index, parameters):
    if not parameters[0]: index = parameters[1]
    return code, index, False

def op_TLT(code, index, parameters):
    if parameters[0] < parameters[1]: code[code[index-1]] = 1
    else: code[code[index-1]] = 0
    return code, index, False

def op_TEQ(code, index, parameters):
    if parameters[0] == parameters[1]: code[code[index-1]] = 1
    else: code[code[index-1]] = 0
    return code, index, False

def op_TRM(code, index, parameters):
    return code, index, True

def run_computer(code):
    done = False
    index = 0
    while not done:
        opcode = f'{code[index]:>05}'[-2:]
        modes = f'{code[index]:>05}'[0:3][::-1]
        increment = get_parameter_count(opcode) + 1
        parameters = code[index+1:index+increment]
        index += increment
        for i, parameter in enumerate(parameters[:]):
            mode = modes[i]
            parameters[i] = set_parameter(code, parameter, mode)
        code, index, done = opcode_handlers()[opcode](code, index, parameters)

with open('input.txt','r') as fh:
    code = [int(i) for i in fh.read().strip('\n').split(',')]

inputval = 5
run_computer(code)