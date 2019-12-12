import itertools

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

print(moons)
while steps < 1000:
    steps += 1
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

print(moons)
totalenergy = 0
for i in moons.keys():
    potential = abs(moons[i][0][0])+abs(moons[i][0][1])+abs(moons[i][0][2])
    kinetic = abs(moons[i][1][0])+abs(moons[i][1][1])+abs(moons[i][1][2])
    total = potential*kinetic
    totalenergy += total
print(totalenergy)