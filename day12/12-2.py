import itertools
import math

with open('input.txt', 'r') as fh:
    data = []
    for line in fh:
        temp = ''
        for i in line.strip():
            if i in '-0123456789 ':
                temp += i
        data.append(temp.split(' '))

moons = {}
for i in range(len(data)):
    moons[i] = [[int(j) for j in data[i]], [0,0,0]]

steps = 0
pairs = list(itertools.combinations(range(4), 2))

def process_timestep():
    for i in pairs:
        for j in range(3):
            if moons[i[0]][0][j] > moons[i[1]][0][j]:
                moons[i[0]][1][j] -= 1
                moons[i[1]][1][j] += 1
            elif moons[i[0]][0][j] < moons[i[1]][0][j]:
                moons[i[0]][1][j] += 1
                moons[i[1]][1][j] -= 1

    for i in moons.keys():
        for j in range(3):
            moons[i][0][j] += moons[i][1][j]

periods = []
for i in range(3):
    testdata = []
    for _ in range(20):
        process_timestep()
        testdata.append(moons[0][0][i])
    data = testdata[:]
    j = 0
    found = False
    while not found:
        j += 1
        process_timestep()
        data.remove(data[0])
        data.append(moons[0][0][i])
        if testdata == data:
            found = True
    periods.append(j)

lcm = periods[0]
for i in periods[1:]:
    lcm = lcm*i // (math.gcd(lcm, i))

print(lcm)