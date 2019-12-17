import itertools

with open('input.txt', 'r') as fh:
    data = [int(i) for i in iter(fh.read().strip())]

basepattern = [[0], [1], [0], [-1]]
for i in range(1, 101):
    newdata = []
    for j in range(len(data)):
        pattern = []
        for k in basepattern:
            pattern.extend((j+1)*k)
        pattern = itertools.cycle(pattern[:])
        next(pattern)
        digit = abs(sum(map(lambda x, y: x * y, data, pattern)))
        newdata.append(int(str(digit)[-1]))
    data = newdata[:]
    print(f'phase {i}: {"".join([str(x) for x in data])[0:8]}')