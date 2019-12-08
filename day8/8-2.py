with open('input.txt', 'r') as fh:
    image = fh.read().strip('\n')

length = 25*6
split = list(map(''.join, zip(*[iter(image)]*length)))

finalimage = ['3']*length
print(finalimage)
for layer in split:
    print(layer)
    for i, pixel in enumerate(layer):
        if pixel != '2':
            if finalimage[i] == '3':
                finalimage[i] = pixel

print(finalimage)
split = list(map(''.join, zip(*[iter(finalimage)]*25)))
for line in split:
    print(line)