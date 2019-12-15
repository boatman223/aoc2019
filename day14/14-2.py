import collections
import math
import itertools

def find_children(target, children):
    sets = (children[target]-spare[target])/recipes[target][0]
    spare[target] = sets * recipes[target][0] - (children[target]-spare[target])
    for i in recipes[target][1].keys():
        if i == 'ORE': return children
        if i in ore.keys():
            children[i] += recipes[target][1][i] * sets
        else:
            children[i] = recipes[target][1][i] * sets
        # print(target, i, children)
        children = find_children(i, children)
    return children

with open('input.txt', 'r') as fh:
    data = [i.strip().replace(',', '').split(' ') for i in fh.readlines()]

recipes = {}
ore = {}
spare = collections.defaultdict(int)
for recipe in data:
    recipes[recipe[-1]] = [int(recipe[-2]), {}]
    if recipe[1] == 'ORE':
        ore[recipe[-1]] = (int(recipe[0]), int(recipe[-2]))
    split = [recipe[i:i+2] for i in range(0, len(recipe), 2)]
    for item in split:
        if item[0] == '=>': break
        recipes[recipe[-1]][1][item[1]] = int(item[0])
# print(recipes)
# print(ore)

total = 0
y = collections.defaultdict(int)
children = collections.defaultdict(int)
for i in recipes['FUEL'][1].keys():
    print(i)
    children[i] += recipes['FUEL'][1][i]
    children = find_children(i, children)
    for j in children:
        if j not in ore.keys(): children[j] = 0
    print(children)
# print(spare)
# print(children)

for i in children.keys():
    if i in ore.keys():
        print(i, children[i])
        total += children[i]/ore[i][1] * ore[i][0]

print(1000000000000//math.ceil(total))