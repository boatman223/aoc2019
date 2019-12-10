def opcode_handlers():
    handlers = {
        1:  opcode_1,
        2:  opcode_2,
        99: opcode_99
    }
    return handlers

def opcode_1(code, inputs, output):
    code[output] = code[inputs[0]] + code[inputs[1]]
    return code, False

def opcode_2(code, inputs, output):
    code[output] = code[inputs[0]] * code[inputs[1]]
    return code, False

def opcode_99(code, inputs, output):
    return code, True

def run_computer(code, noun, verb):
    code[1] = noun
    code[2] = verb
    done = False
    index = 0
    while done == False:       
        opcode = code[index]
        inputs = (code[index+1], code[index+2])
        output = code[index+3]
        code, done = opcode_handlers()[opcode](code, inputs, output)        
        index += 4   
    
    return code[0]

with open('input.txt','r') as fh:
    basecode = [int(i) for i in fh.read().split(',')]

desired_output = 19690720

for noun in range(0,99):
    for verb in range(0,99):
        output = run_computer(basecode[:], noun, verb)
        if output == desired_output:
            break
    if output == desired_output:
        break

print(noun, verb, 100*noun+verb)
