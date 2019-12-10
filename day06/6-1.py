with open('input.txt', 'r') as fh:
    data = {line.strip('\n').split(')')[1]:line.split(')')[0] for line in fh}

def find_orbits(body, total_orbits):
    total_orbits += 1
    try:
        return find_orbits(data[body], total_orbits)
    except:
        return total_orbits

total_orbits = 0
for k, v in data.items():
    total_orbits += find_orbits(v, 0)
print(total_orbits)