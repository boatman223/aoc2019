with open('input.txt', 'r') as fh:
    image = fh.read().strip('\n')

length = 25*6
split = [image[i:i+length] for i in range(0, len(image), length)]

finalimage = ['3']*length
print(finalimage)
for layer in split:
    print(layer)
    for i, pixel in enumerate(layer):
        if pixel != '2':
            if finalimage[i] == '3':
                finalimage[i] = pixel

print(finalimage)
split = [finalimage[i:i+25] for i in range(0, len(finalimage), 25)]
for line in split:
    print(''.join(line))