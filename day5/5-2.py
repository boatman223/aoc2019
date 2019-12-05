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
        '01': opcode_1,
        '02': opcode_2,
        '03': opcode_3,
        '04': opcode_4,
        '05': opcode_5,
        '06': opcode_6,
        '07': opcode_7,
        '08': opcode_8,
        '99': opcode_99
    }
    return handlers

def set_parameter(code, parameter, mode):
    if mode == '0':
        val = code[int(parameter)]
    elif mode == '1':
        val = parameter
    return int(val)

def opcode_1(code, index, parameters, modes):
    for i, parameter in enumerate(parameters[:][0:2]):
        mode = modes[i]
        parameters[i] = set_parameter(code, parameter, mode)
    writeme = parameters[0] + parameters[1]
    code[int(parameters[2])] = str(writeme)
    index += (len(parameters) + 1)
    return code, index, False

def opcode_2(code, index, parameters, modes):
    for i, parameter in enumerate(parameters[:][0:2]):
        mode = modes[i]
        parameters[i] = set_parameter(code, parameter, mode)
    writeme = parameters[0] * parameters[1]
    code[int(parameters[2])] = str(writeme)
    index += (len(parameters) + 1)
    return code, index, False

def opcode_3(code, index, parameters, modes):
    code[int(parameters[0])] = inputval
    index += (len(parameters) + 1)
    return code, index, False

def opcode_4(code, index, parameters, modes):
    mode = modes[0]
    parameters[0] = set_parameter(code, parameters[0], mode)
    print(f'output: {parameters[0]}')
    index += (len(parameters) + 1)
    return code, index, False

def opcode_5(code, index, parameters, modes):
    for i, parameter in enumerate(parameters[:]):
        mode = modes[i]
        parameters[i] = set_parameter(code, parameter, mode)
    if parameters[0]:
        index = parameters[1]
    else:
        index += (len(parameters) + 1)
    return code, index, False

def opcode_6(code, index, parameters, modes):
    for i, parameter in enumerate(parameters[:]):
        mode = modes[i]
        parameters[i] = set_parameter(code, parameter, mode)
    if not parameters[0]:
        index = parameters[1]
    else:
        index += (len(parameters) + 1)
    return code, index, False

def opcode_7(code, index, parameters, modes):
    for i, parameter in enumerate(parameters[:][0:2]):
        mode = modes[i]
        parameters[i] = set_parameter(code, parameter, mode)
    if parameters[0] < parameters[1]:
        code[int(parameters[2])] = 1
    else:
        code[int(parameters[2])] = 0
    index += (len(parameters) + 1)
    return code, index, False

def opcode_8(code, index, parameters, modes):
    for i, parameter in enumerate(parameters[:][0:2]):
        mode = modes[i]
        parameters[i] = set_parameter(code, parameter, mode)
    if parameters[0] == parameters[1]:
        code[int(parameters[2])] = 1
    else:
        code[int(parameters[2])] = 0
    index += (len(parameters) + 1)
    return code, index, False

def opcode_99(code, index, parameters, modes):
    return code, index, True

def run_computer(code):
    done = False
    index = 0
    while done == False:
        opcode = f'{code[index]:>05}'[-2:]
        modes = f'{code[index]:>05}'[0:3][::-1]
        parameter_count = get_parameter_count(opcode)
        increment = parameter_count + 1
        parameters = code[index+1:index+increment]
        code, index, done = opcode_handlers()[opcode](code, index, parameters, modes)

with open('input.txt','r') as fh:
    code = fh.read().strip('\n').split(',')

inputval = '5'
run_computer(code)