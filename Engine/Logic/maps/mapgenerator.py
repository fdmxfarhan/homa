import random
width = 20
height = 15
a = [[-1 for i in range(width)] for j in range(height)]
b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 68, 36, 132, 4]  

for i in range(height):
    for j in range(width-i):
        a[i][j] = b[random.randint(0, len(b)-1)]
        a[height - i -1][width - j -1] = b[random.randint(0, len(b)-1)]

for i in range(len(a)):
    print(str(a[i])+',')