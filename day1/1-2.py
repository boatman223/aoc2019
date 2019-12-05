import math

with open('input.txt','r') as fh:
     modules = [int(line) for line in fh]

def calculate_fuel(mass):
    fuel = (math.floor((mass/3)))-2
    return fuel

total_fuel = 0
for module in modules:
    additional_fuel = calculate_fuel(module)
    while additional_fuel > 0:
        total_fuel += additional_fuel
        additional_fuel = calculate_fuel(additional_fuel)

print(total_fuel)