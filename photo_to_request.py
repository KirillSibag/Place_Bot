import os
import sys
from PIL import Image
jpg_images = [image for image in os.listdir() if image.endswith('.jpg')]
for jpg_image in jpg_images:
    try:
        new_name = jpg_image.split('.')[0] + '.png'
        Image.open(jpg_image).save(new_name)
    except IOError as error:
        print('Couldn\'t read {} '.format(jpg_image))




f = open("result.txt", "w+")

img = Image.open('img.png')
print("X:")
x = int(input())
print("Y:")
y = int(input())

data = []
for i in range(img.size[0]):
    for j in range(img.size[1]):
        col = img.getpixel((i, j))
        data.append(str(i+x) + "," + str(j+y) + "," + str(col[0]) + "," + str(col[1]) + "," + str(col[2]))

for i in data:
    f.write(i + "\n")

f.close()
