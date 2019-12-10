import math
import collections

with open('input.txt', 'r') as fh:
    data = [line.strip() for line in fh]

home = (23, 19)
asteroids = {}
for i, line in enumerate(data):
    for j, space in enumerate(line):
        if space == '#' and (j, i) != home:
            asteroids[(j, i)] = None

for asteroid in asteroids.keys():
    angle = math.atan2(asteroid[0]-home[0], asteroid[1]-home[1])
    distance = math.sqrt(((home[0]-asteroid[0])**2)+((home[1]-asteroid[1])**2))
    asteroids[asteroid] = (angle, distance)

sorteda = {k:v for k, v in sorted(asteroids.items(), key = lambda i: (i[1][0], 1/i[1][1]), reverse=True)}

finalorder = []
while len(sorteda.keys()):
    lastnum = 999
    for k in list(sorteda.keys()):
        if sorteda[k][0] == lastnum: continue
        finalorder.append(k)
        lastnum = sorteda[k][0]
        del sorteda[k]

print(finalorder[199])