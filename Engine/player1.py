import sys
a = input()
print('init confirm')

while True:
    msg = input().split(' ')
    step = int(msg[0])
    x = int(msg[2])
    y = int(msg[3])
    enemyInVision = int(msg[8])

    if(enemyInVision == 0):
        numOfTiles = int(msg[9])
        for i in range(numOfTiles):
            x1 = int(msg[i*3])
            y1 = int(msg[i*3+1])
            state = int(msg[i*3+2])
            print(x1, y1, state, file=sys.stderr)

    print(4)
    