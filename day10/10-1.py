with open('input.txt', 'r') as fh:
    data = [line.strip() for line in fh]
    print(data)

asteroids = set()
for i, line in enumerate(data):
    for j, space in enumerate(line):
        if space == '#':
            asteroids.add((j, i))

most = 0
for a1 in asteroids:
    slopes = set()
    slopes2 = set()
    for a2 in asteroids:
        if a1 == a2: continue
        try:
            slope = (a2[1]-a1[1]) / (a2[0]-a1[0])
        except ZeroDivisionError:
            slope = 999
        if a2[1] > a1[1]:
            slopes.add(slope)
        elif a2[1] < a1[1]:
            slopes2.add(slope)
        else:
            if a2[0] > a1[0]:
                slopes.add(slope)
            else:
                slopes2.add(slope)
    if len(slopes)+len(slopes2) > most:
        most = len(slopes)+len(slopes2)

print(most)