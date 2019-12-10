import math

with open('input.txt','r') as fh:
     modules = [int(line) for line in fh]

fuel = 0
for mass in modules:
    fuel += (math.floor((mass/3)))-2
    
print(fuel)