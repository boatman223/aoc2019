import math

with open('input.txt', 'r') as fh:
    data = [line.strip() for line in fh]

asteroids = set()
for i, line in enumerate(data):
    for j, space in enumerate(line):
        if space == '#':
            asteroids.add((j, i))

most = 0
for a1 in asteroids:
    slopes = set()
    for a2 in asteroids:
        if a1 == a2: continue
        angle = math.atan2(a2[1]-a1[1], a2[0]-a1[0])
        slopes.add(angle)
    if len(slopes) > most:
        most = len(slopes)

print(most)