import sys
import random
############ Initial Data
init_msg = input().split(' ')
print('init confirm')
height = int(init_msg[1])
width = int(init_msg[2])
x = int(init_msg[3])
y = int(init_msg[4])
health = int(init_msg[5])
bombRange = int(init_msg[6])
trapCount = int(init_msg[7])
vision = int(init_msg[8])
bombDelay = int(init_msg[9])
maxBombRange = int(init_msg[10])
deadZoneStartingStep = int(init_msg[11])
deadZoneExpansionDelay = int(init_msg[12])
maxStep = int(init_msg[13])

def log(msg):
    pass
    # print(msg, file=sys.stderr)

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class Player:
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.traps = []
        self.lastAction = -1
        self.healthUpgradeCount = 0
        self.bombRange = 0
        self.trapCount = 0
        self.enemyInVision = False
        self.destination = {'x': x, 'y': y}
        self.target = 'none'
        self.placedTrap = False
        self.runDirection = 'up'
        self.runing = True
        self.placeEndBomb = False
    def move(self, direction):
        direction = direction.lower()
        if(direction == 'left'):
            # log('moved left')
            print(0)
        elif(direction == 'right'):
            # log('moved right')
            print(1)
        elif(direction == 'up'):
            # log('moved up')
            print(2)
        elif(direction == 'down'):
            # log('moved down')
            print(3)
        else:
            # log('stay')
            print(4)
    def placeBomb(self):
        gameMap.setTile(self.x, self.y, 4)
        print(5)
    def placeTrap(self, direction):
        self.placedTrap = True
        direction = direction.lower()
        if(direction == 'left'):
            print(6)
            self.traps.append({'x': self.x, 'y': self.y-1})
        elif(direction == 'right'):
            print(7)
            self.traps.append({'x': self.x, 'y': self.y+1})
        elif(direction == 'up'):
            print(8)
            self.traps.append({'x': self.x-1, 'y': self.y})
        elif(direction == 'down'):
            print(9)
            self.traps.append({'x': self.x+1, 'y': self.y})
    def printPos(self):
        log(str(self.x) + ' ' + str(self.y))
    def explore(self):
        if(gameMap.isWalkable(me.x, me.y+1) and self.y < gameMap.width/2 and self.lastAction != 0):
            self.destination = {'x': self.x, 'y': self.y+1}
        elif(gameMap.isWalkable(me.x+1, me.y) and self.x < gameMap.height/2 and self.lastAction != 2):
            self.destination = {'x': self.x+1, 'y': self.y}
        elif(gameMap.isWalkable(me.x, me.y-1) and self.y > gameMap.width/2 and self.lastAction != 1):
            self.destination = {'x': self.x, 'y': self.y-1}
        elif(gameMap.isWalkable(me.x-1, me.y) and self.x > gameMap.height/2 and self.lastAction != 3):
            self.destination = {'x': self.x-1, 'y': self.y}
        elif(gameMap.isWalkable(me.x, me.y+1) and self.lastAction != 0):
            self.destination = {'x': self.x, 'y': self.y+1}
        elif(gameMap.isWalkable(me.x+1, me.y) and self.lastAction != 2):
            self.destination = {'x': self.x+1, 'y': self.y}
        elif(gameMap.isWalkable(me.x, me.y-1) and self.lastAction != 1):
            self.destination = {'x': self.x, 'y': self.y-1}
        elif(gameMap.isWalkable(me.x-1, me.y) and self.lastAction != 3):
            self.destination = {'x': self.x-1, 'y': self.y}
        else:
            self.destination = {'x': self.x, 'y': self.y}
        self.target = 'explore'
    def goToDestination(self, gameMap):
        if(me.placeEndBomb):
            self.move('stay')
            return
        x = self.destination['x']
        y = self.destination['y']
        path = gameMap.findPath(self.getPos(), self.destination)
        # log('path: ' + str(path) + ' x:' + str(x) + ' y:' + str(y))
        if(x == self.x and y == self.y):
            if(self.target == 'placeBomb'):
                self.placeBomb()
            elif('placeTrap' in self.target):
                self.placeTrap(self.target[9:])
            elif(self.target == 'deadZone'):
                if(gameMap.stepToDeadZone(stepCount, x, y) < 10):
                    self.placeBomb()
                    self.placeEndBomb = True
                elif(gameMap.isWalkable(x-1, y) and not gameMap.isTrap(x-1, y)):
                    self.placeTrap('up')
                elif(gameMap.isWalkable(x+1, y) and not gameMap.isTrap(x+1, y)):
                    self.placeTrap('down')
                elif(gameMap.isWalkable(x, y-1) and not gameMap.isTrap(x, y-1)):
                    self.placeTrap('left')
                elif(gameMap.isWalkable(x, y+1) and not gameMap.isTrap(x, y+1)):
                    self.placeTrap('right')
                else:
                    self.placeTrap('up')
            else: 
                me.move('stay')
        elif(path):
            x = path[1][0]
            y = path[1][1]
            if(self.y < y):
                self.move('right')
            elif(self.y > y):
                self.move('left')
            elif(self.x < x):
                self.move('down')
            elif(self.x > x):
                self.move('up')
            else:
                self.move('stay')
        else:
            # log('no path found to ' + str(x) + ', ' + str(y))
            direction = gameMap.getNotWalkedTile(self.x, self.y, self.lastAction)
            if(self.target == 'deadZone' and self.runing):
                if(self.y < y):
                    if(gameMap.isWalkable(self.x, self.y+1)):
                        self.move('right')
                    else: 
                        if(not gameMap.isWalkable(self.x-1, self.y)):
                            self.runDirection = 'down'
                        if(not gameMap.isWalkable(self.x+1, self.y)):
                            self.runDirection = 'up'
                        if(not gameMap.isWalkable(self.x-1, self.y) and not gameMap.isWalkable(self.x+1, self.y)):
                            self.move('left')
                            self.runing = False
                        else:
                            self.move(self.runDirection)
                else:
                    if(gameMap.isWalkable(self.x, self.y-1)):
                        self.move('left')
                    else: 
                        if(not gameMap.isWalkable(self.x-1, self.y)):
                            self.runDirection = 'down'
                        if(not gameMap.isWalkable(self.x+1, self.y)):
                            self.runDirection = 'up'
                        if(not gameMap.isWalkable(self.x-1, self.y) and not gameMap.isWalkable(self.x+1, self.y)):
                            self.move('right')
                            self.runing = False
                        else:
                            self.move(self.runDirection)
                    # else:
            elif(direction != (0, 0)):
                self.move(gameMap.tupleToDirection(direction))
            # if  (self.y < y and gameMap.isWalkable(self.x, self.y+1) and self.lastAction != 0):
            #     self.move('right')
            # elif(self.y > y and gameMap.isWalkable(self.x, self.y-1) and self.lastAction != 1):
            #     self.move('left')
            # elif(self.x < x and gameMap.isWalkable(self.x+1, self.y) and self.lastAction != 2):
            #     self.move('down')
            # elif(self.x > x and gameMap.isWalkable(self.x-1, self.y) and self.lastAction != 3):
            #     self.move('up')
            elif(gameMap.isWalkable(self.x, self.y+1) and self.lastAction != 0):
                self.move('right')
            elif(gameMap.isWalkable(self.x, self.y-1) and self.lastAction != 1):
                self.move('left')
            elif(gameMap.isWalkable(self.x+1, self.y) and self.lastAction != 2):
                self.move('down')
            elif(gameMap.isWalkable(self.x-1, self.y) and self.lastAction != 3):
                self.move('up')
            else:
                me.move('stay')
    def getPos(self):
        return({'x': self.x, 'y': self.y})
        
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[-1 for i in range(width)] for j in range(height)]
        self.walkedTiles = [[0 for i in range(width)] for j in range(height)]
        self.bombRange = 2
        self.traps = []
        # 0: Tile is in dead zone
        # 1: Fire (explosion side effect)
        # 2: Box
        # 3: Wall
        # 4: Bomb
        # 5: Bomb range upgrade
        # 6: Health upgrade
        # 7: Trap upgrade
        # 8: A player
    def actionToDirection(self, action):
        if(action == 0):
            return 'left'
        elif(action == 1):
            return 'right'
        elif(action == 2):
            return 'up'
        elif(action == 3):
            return 'down'
        else:
            return 'stay'
    def setWalkedTiles(self, x, y):
        self.walkedTiles[x][y] += 1
    def getNotWalkedTile(self, x, y, action):
        myRange = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        lastDirection = self.actionToDirection(action)
        if lastDirection == 'left':
            myRange = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        elif lastDirection == 'right':
            myRange = [(0, -1), (1, 0), (-1, 0), (0, 1)]
        elif lastDirection == 'up':
            myRange = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        elif lastDirection == 'down':
            myRange = [(-1, 0), (0, 1), (0, -1), (1, 0)]

        minWalked = 9999
        direction = (0, 0)
        for i in myRange:
            newx = x + i[0]
            newy = y + i[1]
            if(newx < self.height and newx >= 0 and newy < self.width and newy >= 0): 
                if self.walkedTiles[newx][newy] <= minWalked and self.isWalkable(newx, newy):
                    minWalked = self.walkedTiles[newx][newy]
                    direction = i
        return direction
    def setTile(self, x, y, state):
        self.map[x][y] = state
    def getTile(self, x, y):
        if(x >= self.height or x < 0 or y >= self.width or y < 0): 
            # log('unexpected cordinates: ' + str(x) + ', ' + str(y))
            return -1
        state = self.map[x][y]
        if(state == -1):
            return -1
        state = bin(state)[2:]
        state = '0' *(9-len(state)) + state
        state = state[::-1]
        return state
    def isWalkable(self, x, y):
        if(y>=self.width or x>=self.height):
            return False
        state = self.getTile(x, y)
        # log(str(x) + ' ' + str(y) + ' ' + str(state))
        if(state == -1):
            return False
        elif(state[0] == '1'):
            return False
        elif(state[2] == '1'): 
            return False
        elif(state[3] == '1'): 
            return False
        elif(state[4] == '1'): 
            return False
        elif(state[8] == '1' and not (x == me.x and y == me.y)): 
            return False
        if({'x': x, 'y': y} in self.traps):
            return False
        return True
    def isPowerup(self, x, y):
        if(y>=self.width or x>=self.height):
            return False
        state = self.getTile(x, y)
        if(state == -1):
            return False
        if(state[0] == '1'):
            return False
        elif(state[5] == '1'): 
            return True
        elif(state[6] == '1'): 
            return True
        elif(state[7] == '1'): 
            return True
        return False
    def isBox(self, x, y):
        state = self.getTile(x, y)
        if state != -1:
            if(state[2] == '1' and state[0] != '1'):
                return True
        return False
    def isBomb(self, x, y):
        state = self.getTile(x, y)
        if state != -1:
            if(state[4] == '1'):
                return True
        return False
    def isPlayer(self, x, y):
        state = self.getTile(x, y)
        if state != -1:
            if(state[8] == '1' and state[0] != '1'):
                return True
        return False
    def tupleToDirection(self, tup):
        if(tup == (0, 1)):
            return 'right'
        elif(tup == (1, 0)):
            return 'down'
        elif(tup == (0, -1)):
            return 'left'
        elif(tup == (-1, 0)):
            return 'up'
    def directionToTuple(self, direction):
        if(direction == 'right'):
            return (0, 1)
        elif(direction == 'down'):
            return (1, 0)
        elif(direction == 'left'):
            return (0, -1)
        elif(direction == 'up'):
            return (-1, 0)
    def isEnemyClose(self, player):
        for pos in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            if(self.isPlayer(player.x + pos[0], player.y + pos [1])):
                return self.tupleToDirection(pos)
        return False
    def findNearestBox(self, x, y):
        boxes = []
        cnt = 0
        minDist = 9999
        minIndex = 0
        for i in range(self.height):
            for j in range(self.width):
                if(self.isBox(i, j)):
                    dist = abs(i-x) + abs(j-y)
                    boxes.append({'x': i, 'y': j, 'distance': dist})
                    bestPlaceForBomb = self.findBestPlaceForBomb({'x': i, 'y': j})
                    if(bestPlaceForBomb):
                        if(dist <= minDist and self.findPath({'x': x, 'y': y}, bestPlaceForBomb)): 
                            minDist = dist
                            minIndex = cnt
                    cnt += 1
        if cnt == 0: return False
        return boxes[minIndex]
    def findNearestBomb(self, x, y):
        bombs = []
        cnt = 0
        minDist = 9999
        minIndex = 0
        for i in range(self.height):
            for j in range(self.width):
                if(self.isBomb(i, j)):
                    dist = abs(i-x) + abs(j-y)
                    bombs.append({'x': i, 'y': j, 'distance': dist})
                    if(dist < minDist): 
                        minDist = dist
                        minIndex = cnt
                    cnt += 1
        if cnt == 0: return False
        return bombs[minIndex]
    def findNearestPowerup(self, x, y):
        powerups = []
        cnt = 0
        minDist = 9999
        minIndex = 0
        for i in range(self.height):
            for j in range(self.width):
                if(self.isPowerup(i, j)):
                    dist = abs(i-x) + abs(j-y)
                    powerups.append({'x': i, 'y': j, 'distance': dist})
                    if(dist < minDist): 
                        minDist = dist
                        minIndex = cnt
                    cnt += 1
        if cnt == 0: return False
        return powerups[minIndex]
    def isInrange(self, box, bomb):
        if(box['x'] == bomb['x']):
            if(box['y'] > bomb['y']):
                for i in range(bomb['y'] + 1, box['y']):
                    if(not self.isWalkable(box['x'], i)):
                        return False
            else:
                for i in range(box['y'] + 1, bomb['y']):
                    if(not self.isWalkable(box['x'], i)):
                        return False
        elif(box['y'] == bomb['y']):
            if(box['x'] > bomb['x']):
                for i in range(bomb['x'] + 1, box['x']):
                    if(not self.isWalkable(i, box['y'])):
                        return False
            else:
                for i in range(box['x'] + 1, bomb['x']):
                    if(not self.isWalkable(i, box['y'])):
                        return False
        else:
            return False
        return True
    def findBestPlaceForBomb(self, box):
        # log(self.bombRange)
        allDestinations = []
        for i in range(1, self.bombRange+1):
            destinations = []
            if(self.isWalkable(box['x']-i, box['y'])):
                destinations.append({'x': box['x']-i, 'y': box['y']})
            if(self.isWalkable(box['x']+i, box['y'])):
                destinations.append({'x': box['x']+i, 'y': box['y']})
            if(self.isWalkable(box['x'], box['y']+i)):
                destinations.append({'x': box['x'], 'y': box['y']+i})
            if(self.isWalkable(box['x'], box['y']-i)):
                destinations.append({'x': box['x'], 'y': box['y']-i})
            # log(destinations)
            for destination in destinations:
                if(self.findBestPlaceForHide(destination) and self.isInrange(box, destination)):
                    path = self.findPath(me.getPos(), destination)
                    if(path != None):
                        destination['distance'] = len(path)
                        allDestinations.append(destination)
        if(len(allDestinations) == 0):
            return False
        minDist = 9999
        minIndex = 0
        for i in range(len(allDestinations)):
            if(allDestinations[i]['distance'] < minDist):
                minDist = allDestinations[i]['distance']
                minIndex = i
        # log(allDestinations)
        # log(allDestinations[minIndex])
        return allDestinations[minIndex]
    def findSecondPlaceForBomb(self, box):
        if(self.isPathWalkable(box, me.bombRange, 'down')):
            return {'x': box['x']+me.bombRange, 'y': box['y']}
        elif(self.isPathWalkable(box, me.bombRange, 'up')):
            return {'x': box['x']-me.bombRange, 'y': box['y']}
        elif(self.isPathWalkable(box, me.bombRange, 'right')):
            return {'x': box['x'], 'y': box['y']+me.bombRange}
        elif(self.isPathWalkable(box, me.bombRange, 'left')):
            return {'x': box['x'], 'y': box['y']-me.bombRange}
        return False
    def isPathWalkable(self, source, numberOfTiles, direction):
        if(direction == 'left'):
            for i in range(numberOfTiles):
                if(not self.isWalkable(source['x'], source['y']-i)):
                    return False
        elif(direction == 'right'):
            for i in range(numberOfTiles):
                if(not self.isWalkable(source['x'], source['y']+i)):
                    return False
        elif(direction == 'up'):
            for i in range(numberOfTiles):
                if(not self.isWalkable(source['x']-i, source['y'])):
                    return False
        elif(direction == 'down'):
            for i in range(numberOfTiles):
                if(not self.isWalkable(source['x']+i, source['y'])):
                    return False
        return True
    def findSimplePath(self, source, target):
        if(abs(source['x'] - target['x']) < abs(source['y'] - target['y'])):
            if(source['y'] < target['y']):
                for i in range(source['y'], target['y']):
                    if(not self.isWalkable(source['x'], i)):
                        return False
                if(source['x'] < target['x']):
                    for i in range(source['x'], target['x']):
                        if(not self.isWalkable(i, target['y'])):
                            return False
                else:
                    for i in range(target['x'], source['x']):
                        if(not self.isWalkable(i, target['y'])):
                            return False
            else:
                for i in range(target['y'], source['y']):
                    if(not self.isWalkable(source['x'], i)):
                        return False
                if(source['x'] < target['x']):
                    for i in range(source['x'], target['x']):
                        if(not self.isWalkable(i, target['y'])):
                            return False
                else:
                    for i in range(target['x'], source['x']):
                        if(not self.isWalkable(i, target['y'])):
                            return False
        else:
            if(source['x'] < target['x']):
                for i in range(source['x'], target['x']):
                    if(not self.isWalkable(i, source['x'])):
                        return False
                if(source['y'] < target['y']):
                    for i in range(source['y'], target['y']):
                        if(not self.isWalkable(target['x'], i)):
                            return False
                else:
                    for i in range(target['y'], source['y']):
                        if(not self.isWalkable(target['x'], i)):
                            return False
            else:
                for i in range(target['x'], source['x']):
                    if(not self.isWalkable(i, source['x'])):
                        return False
                if(source['y'] < target['y']):
                    for i in range(source['y'], target['y']):
                        if(not self.isWalkable(target['x'], i)):
                            return False
                else:
                    for i in range(target['y'], source['y']):
                        if(not self.isWalkable(target['x'], i)):
                            return False
        return True
    def findBestPlaceForHide(self, bomb):
        for i in range(bomb['x'], bomb['x'] + self.bombRange):
            if(i != bomb['x']):
                if(self.isWalkable(i, bomb['y']+1) and self.findPath(bomb, {'x': i, 'y': bomb['y']+1}) != None):
                    return {'x': i, 'y': bomb['y']+1}
                elif(self.isWalkable(i, bomb['y']-1) and self.findPath(bomb, {'x': i, 'y': bomb['y']-1}) != None):
                    return {'x': i, 'y': bomb['y']-1}
        for i in range(bomb['x'], bomb['x'] - self.bombRange, -1):
            if(i != bomb['x']):
                if(self.isWalkable(i, bomb['y']+1) and self.findPath(bomb, {'x': i, 'y': bomb['y']+1}) != None):
                    return {'x': i, 'y': bomb['y']+1}
                elif(self.isWalkable(i, bomb['y']-1) and self.findPath(bomb, {'x': i, 'y': bomb['y']-1}) != None):
                    return {'x': i, 'y': bomb['y']-1}
        for i in range(bomb['y'], bomb['y'] + self.bombRange):
            if(i != bomb['y']):
                if(self.isWalkable(bomb['x']+1, i) and self.findPath(bomb, {'x': bomb['x']+1, 'y': i}) != None):
                    return {'x': bomb['x']+1, 'y': i}
                elif(self.isWalkable(bomb['x']-1, i) and self.findPath(bomb, {'x': bomb['x']-1, 'y': i}) != None):
                    return {'x': bomb['x']-1, 'y': i}
        for i in range(bomb['y'], bomb['y'] - self.bombRange, -1):
            if(i != bomb['y']):
                if(self.isWalkable(bomb['x']+1, i) and self.findPath(bomb, {'x': bomb['x']+1, 'y': i}) != None):
                    return {'x': bomb['x']+1, 'y': i}
                elif(self.isWalkable(bomb['x']-1, i) and self.findPath(bomb, {'x': bomb['x']-1, 'y': i}) != None):
                    return {'x': bomb['x']-1, 'y': i}
        return False
    def findPath(self, source, target):
        start =(source['x'], source['y'])
        end = (target['x'], target['y'])
        myMap = self.map.copy()
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0   

        # Initialize both open and closed list
        open_list = []
        closed_list = []
        cnt = 0
        # Add the start node
        open_list.append(start_node)
        while len(open_list) > 0 and cnt < int((width*height)/4):
            cnt += 1
            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)
            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path
            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                # Make sure within range
                if node_position[0] > self.height or node_position[0] < 0 or node_position[1] > self.width or node_position[1] < 0:
                    continue
                # Make sure walkable terrain
                if not self.isWalkable(node_position[0], node_position[1]) :
                    continue
                # Create new node
                new_node = Node(current_node, node_position)
                children.append(new_node)

            for child in children:
                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue
                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h
                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue
                # Add the child to the open list
                open_list.append(child)
        return None
    def isTrap(self, x, y):
        for trap in self.traps:
            if(trap['x'] == x and trap['y'] == y):
                return True
        return False
    def findBestDirectionForTrap(self, me, enemy):
        minDist = 9999
        direction = (0, 0)
        for i in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newPos = {'x': me.x + i[0], 'y': me.y + i[1]}
            path = self.findPath(enemy.getPos(), newPos)
            if(not self.isTrap(newPos['x'], newPos['y']) and path != None):
                if(len(path) < minDist):
                    minDist = len(path)
                    direction = i
        if(direction == (0, 0)):
            return False
        return self.directionToTuple(direction)
    def stepToDeadZone(self,currentStep,x,y):
        DZSS = deadZoneStartingStep
        DZED = deadZoneExpansionDelay
        LowestDistToborder=min([x+1, y+1, self.width - y, self.height - x])
        stepToDeadZone=(DZSS +LowestDistToborder*DZED )-currentStep
        return stepToDeadZone
    def resetAllBombs(self):
        for i in range(self.height):
            for j in range(self.width):
                if(self.isBomb(i, j)):
                    gameMap.map[i][j] = -1
    def getCenter(self):
        for pos in [(0, 0), (0, 1), (0, -1), (0, 2), (0, -2), (1, 0), (-1, 0), (1, 1), (-1, -1)]:
            x = int(self.height/2) + pos[0]
            y = int(self.width/2)  + pos[1]
            if(self.isWalkable(x, y)):
                return {'x': x, 'y': y}
        return {'x': self.height/2, 'y': self.width/2}
    def printMap(self):
        for i in range(len(self.map)):
            log(self.map[i])
gameMap = Map(width, height)

me = Player(x, y, health)
enemy = Player(height-x - 1, width-y - 1, health)
stepCount = 0
log(init_msg)


def AI():
    gameMap.setWalkedTiles(me.x, me.y)
    # log(gameMap.stepToDeadZone(stepCount, me.x, me.y))
    directionForTrap = gameMap.findBestDirectionForTrap(me, enemy)
    nearestBox = gameMap.findNearestBox(me.x, me.y)
    nearestBomb = gameMap.findNearestBomb(me.x, me.y)
    nearestPowerup = gameMap.findNearestPowerup(me.x, me.y)
    enemyClose = gameMap.isEnemyClose(me)
    centerPos = gameMap.getCenter()
    pathToCenter = gameMap.findPath(me.getPos(), centerPos)
    if(pathToCenter == None): pathToCenter = [0] * gameMap.width


    if(enemyClose and me.trapCount > 0):
        me.destination = me.getPos()
        me.target = 'placeTrap' + enemyClose
    elif(stepCount > deadZoneStartingStep-(len(pathToCenter)+5)):
        log(centerPos)
        log(pathToCenter)
        gameMap.printMap()
        log(' ')
        me.destination = centerPos
        me.target = 'deadZone'
    elif(me.enemyInVision and not me.placedTrap and directionForTrap and me.trapCount > 0):
        # log('place trap: ' + str(directionForTrap))
        me.destination = me.getPos()
        me.target = 'placeTrap' + directionForTrap
    elif(nearestBomb):
        destination = gameMap.findBestPlaceForHide(nearestBomb)
        if(destination):
            # log('hide: ' + str(destination))
            me.destination = destination
            me.target = 'hide'
        else:
            # log('explore1')
            me.explore()
    elif(nearestPowerup and gameMap.findPath(me.getPos(), nearestPowerup) != None):
        # log('get powerup: ' + str(nearestPowerup))
        me.destination = nearestPowerup
        me.target = 'placeBomb'
    elif(nearestBox):
        destination = gameMap.findBestPlaceForBomb(nearestBox)
        if(destination and gameMap.findBestPlaceForHide(destination)):
            # log('goto box: ' + str(destination))
            me.destination = destination
            me.target = 'placeBomb'
        else:
            # log('explore2')
            me.explore()
    else:
        # log('explore3')
        me.explore()
    
    me.goToDestination(gameMap)
    # log(stepCount)

while True:
    gameMap.resetAllBombs()
    state_msg = input()
    # log(state_msg)
    state_msg = state_msg.split(' ')
    if 'term' in state_msg:
        break
    stepCount = int(state_msg[0])
    me.lastAction = int(state_msg[1])
    me.x = int(state_msg[2])
    me.y = int(state_msg[3])
    me.health = int(state_msg[4])
    me.healthUpgradeCount = int(state_msg[5])
    me.bombRange = int(state_msg[6])
    enemy.bombRange = int(state_msg[6])
    me.trapCount = int(state_msg[7])
    if(int(state_msg[8]) == 0):
        me.enemyInVision = False
        me.placedTrap = False
        numberOfTilesInVision = int(state_msg[9])
        for i in range(10, 10+numberOfTilesInVision*3, 3):
            x = int(state_msg[i])
            y = int(state_msg[i+1])
            gameMap.setTile(x, y, int(state_msg[i+2]))
    else:
        me.enemyInVision = True
        enemy.x = int(state_msg[9])
        enemy.y = int(state_msg[10])
        enemy.health = int(state_msg[11])
        numberOfTilesInVision = int(state_msg[12])
        for i in range(13, 13+numberOfTilesInVision*3, 3):
            x = int(state_msg[i])
            y = int(state_msg[i+1])
            gameMap.setTile(x, y, int(state_msg[i+2]))
    # if(stepCount == 2):
    #     log(gameMap.findPath(me.getPos(), {'x': 1, 'y': 9}))
    # me.move('stay')
    AI()
    gameMap.traps = me.traps
    
    # log(gameMap.map)


    