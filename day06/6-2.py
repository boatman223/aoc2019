with open('input.txt', 'r') as fh:
    data = {line.strip('\n').split(')')[1]:line.split(')')[0] for line in fh}

def find_orbits(body, orbit_list):
    orbit_list.add(body)
    try:
        return find_orbits(data[body], orbit_list)
    except:
        return orbit_list

orbit_list1 = find_orbits('YOU', set())
orbit_list2 = find_orbits('SAN', set())
print(len(orbit_list1 ^ orbit_list2) - 2)