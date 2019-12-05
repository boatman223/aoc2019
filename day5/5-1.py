def get_parameter_count(opcode):
    count = {
        '01': 3,
        '02': 3,
        '03': 1,
        '04': 1,
        '99': 0
    }
    return count[opcode]

def opcode_handlers():
    handlers = {
        '01': opcode_1,
        '02': opcode_2,
        '03': opcode_3,
        '04': opcode_4,
        '99': opcode_99
    }
    return handlers

def set_parameter(code, parameter, mode):
    if mode == '0':
        val = code[int(parameter)]
    elif mode == '1':
        val = parameter
    return int(val)

def opcode_1(code, parameters, modes):
    for i, parameter in enumerate(parameters[:][0:2]):
        mode = modes[i]
        parameters[i] = set_parameter(code, parameter, mode)
    writeme = parameters[0] + parameters[1]
    code[int(parameters[2])] = str(writeme)
    return code, False

def opcode_2(code, parameters, modes):
    for i, parameter in enumerate(parameters[:][0:2]):
        mode = modes[i]
        parameters[i] = set_parameter(code, parameter, mode)
    writeme = parameters[0] * parameters[1]
    code[int(parameters[2])] = str(writeme)
    return code, False

def opcode_3(code, parameters, modes):
    code[int(parameters[0])] = inputval
    return code, False

def opcode_4(code, parameters, modes):
    mode = modes[0]
    parameters[0] = set_parameter(code, parameters[0], mode)
    print(f'output: {parameters[0]}')
    return code, False

def opcode_99(code, parameters, modes):
    return code, True

def run_computer(code):
    done = False
    index = 0
    while done == False:
        opcode = f'{code[index]:>05}'[-2:]
        modes = f'{code[index]:>05}'[0:3][::-1]
        parameter_count = get_parameter_count(opcode)
        increment = parameter_count + 1
        parameters = code[index+1:index+increment]
        code, done = opcode_handlers()[opcode](code, parameters, modes)
        index += increment

with open('input.txt','r') as fh:
    code = fh.read().strip('\n').split(',')

inputval = '1'
run_computer(code)