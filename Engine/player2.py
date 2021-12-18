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
    print(msg, file=sys.stderr)

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
    def move(self, direction):
        direction = direction.lower()
        if(direction == 'left'):
            log('moved left')
            print(0)
        elif(direction == 'right'):
            log('moved right')
            print(1)
        elif(direction == 'up'):
            log('moved up')
            print(2)
        elif(direction == 'down'):
            log('moved down')
            print(3)
        else:
            log('stay')
            print(4)
    def placeBomb(self):
        gameMap.setTile(self.x, self.y, 4)
        print(5)
    def placeTrap(self, direction):
        direction = direction.lower()
        if(direction == 'left'):
            print(6)
            self.traps.append(self.x-1, self.y)
            gameMap.setTile(self.x-1, self.y, 9)
        elif(direction == 'right'):
            print(7)
            self.traps.append(self.x+1, self.y)
            gameMap.setTile(self.x+1, self.y, 9)
        elif(direction == 'up'):
            print(8)
            self.traps.append(self.x, self.y-1)
            gameMap.setTile(self.x, self.y-1, 9)
        elif(direction == 'down'):
            print(9)
            self.traps.append(self.x, self.y+1)
            gameMap.setTile(self.x, self.y+1, 9)
    def checkTrap(self, x, y):
        pass
    def checkBomb(self):
        pass
    def printPos(self):
        log(str(self.x) + ' ' + str(self.y))
    def explore(self):
        if(gameMap.isWalkable(me.x, me.y+1) and self.lastAction != 0):
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
        x = self.destination['x']
        y = self.destination['y']
        path = gameMap.findPath(self.getPos(), self.destination)
        log('path: ' + str(path) + ' x:' + str(x) + ' y:' + str(y))
        if(x == self.x and y == self.y):
            if(self.target == 'placeBomb'):
                self.placeBomb()
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
            if(gameMap.isWalkable(self.x, self.y+1)):
                self.move('right')
            elif(y and gameMap.isWalkable(self.x, self.y-1)):
                self.move('left')
            elif(gameMap.isWalkable(self.x+1, self.y)):
                self.move('down')
            elif(gameMap.isWalkable(self.x-1, self.y)):
                self.move('up')
            else:
                if(self.x == x):
                    self.move('right')
                elif(self.y == y):
                    self.move('down')
                else:
                    me.move('stay')
    def getPos(self):
        return({'x': self.x, 'y': self.y})
    def knifePlayer(self,x,y):
        dir=gameMap.giveDirection(x,y)
        self.placeTrap(dir)          

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[-1 for i in range(width)] for j in range(height)]
        self.bombRange = 2
        # 0: Tile is in dead zone
        # 1: Fire (explosion side effect)
        # 2: Box
        # 3: Wall
        # 4: Bomb
        # 5: Bomb range upgrade
        # 6: Health upgrade
        # 7: Trap upgrade
        # 8: A player
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
        # elif(state[8] == '1'): 
        #     return False
        return True
    def isPowerup(self, x, y):
        if(y>=self.width or x>=self.height):
            return False
        state = self.getTile(x, y)
        if(state == -1):
            return False
        elif(state[5] == '1'): 
            return True
        elif(state[6] == '1'): 
            return True
        elif(state[7] == '1'): 
            return True
        return False
    def findNearestBox(self, x, y):
        boxes = []
        cnt = 0
        minDist = 9999
        minIndex = 0
        for i in range(self.width):
            for j in range(self.height):
                state = self.getTile(i, j)
                if state != -1:
                    if(state[2] == '1'):
                        dist = abs(i-x) + abs(j-y)
                        boxes.append({'x': i, 'y': j, 'distance': dist})
                        if(dist < minDist): 
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
        for i in range(self.width):
            for j in range(self.height):
                state = self.getTile(i, j)
                if state != -1:
                    if(state[4] == '1'):
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
        for i in range(self.width):
            for j in range(self.height):
                if(self.isPowerup(i, j)):
                    dist = abs(i-x) + abs(j-y)
                    powerups.append({'x': i, 'y': j, 'distance': dist})
                    if(dist < minDist): 
                        minDist = dist
                        minIndex = cnt
                    cnt += 1
        if cnt == 0: return False
        return powerups[minIndex]
    def findBestPlaceForBomb(self, box):
        dest = False
        if(me.x < box['x']):
            if(self.isWalkable(box['x']-1, box['y'])):
                dest =  {'x': box['x']-1, 'y': box['y']}
            elif(self.isWalkable(box['x']+1, box['y'])):
                dest =  {'x': box['x']+1, 'y': box['y']}
            elif(self.isWalkable(box['x'], box['y']+1)):
                dest =  {'x': box['x'], 'y': box['y']+1}
            elif(self.isWalkable(box['x'], box['y']-1)):
                dest =  {'x': box['x'], 'y': box['y']-1}
        else:
            if(self.isWalkable(box['x']+1, box['y'])):
                dest =  {'x': box['x']+1, 'y': box['y']}
            elif(self.isWalkable(box['x']-1, box['y'])):
                dest =  {'x': box['x']-1, 'y': box['y']}
            elif(self.isWalkable(box['x'], box['y']+1)):
                dest =  {'x': box['x'], 'y': box['y']+1}
            elif(self.isWalkable(box['x'], box['y']-1)):
                dest =  {'x': box['x'], 'y': box['y']-1}
        if(dest):
            if(self.findBestPlaceForHide(dest)):
                return dest
            else:
                if(me.x < box['x']):
                    if(self.isWalkable(box['x']-2, box['y'])):
                        dest =  {'x': box['x']-2, 'y': box['y']}
                    elif(self.isWalkable(box['x']+2, box['y'])):
                        dest =  {'x': box['x']+2, 'y': box['y']}
                    elif(self.isWalkable(box['x'], box['y']+2)):
                        dest =  {'x': box['x'], 'y': box['y']+2}
                    elif(self.isWalkable(box['x'], box['y']-2)):
                        dest =  {'x': box['x'], 'y': box['y']-2}
                else:
                    if(self.isWalkable(box['x']+2, box['y'])):
                        dest =  {'x': box['x']+2, 'y': box['y']}
                    elif(self.isWalkable(box['x']-2, box['y'])):
                        dest =  {'x': box['x']-2, 'y': box['y']}
                    elif(self.isWalkable(box['x'], box['y']+2)):
                        dest =  {'x': box['x'], 'y': box['y']+2}
                    elif(self.isWalkable(box['x'], box['y']-2)):
                        dest =  {'x': box['x'], 'y': box['y']-2}
                if(dest):
                    if(self.findBestPlaceForHide(dest)):
                        return dest
                    else:
                        return False
        return False
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
        for i in range(bomb['x'] - self.bombRange, bomb['x'] + self.bombRange):
            if(i != bomb['x']):
                if(self.isWalkable(i, bomb['y']+1) and self.findPath(bomb, {'x': i, 'y': bomb['y']+1}) != None):
                    return {'x': i, 'y': bomb['y']+1}
                elif(self.isWalkable(i, bomb['y']-1) and self.findPath(bomb, {'x': i, 'y': bomb['y']-1}) != None):
                    return {'x': i, 'y': bomb['y']-1}
        for i in range(bomb['y'] - self.bombRange, bomb['y'] + self.bombRange):
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
        while len(open_list) > 0 and cnt < width*height:
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
    def giveDirection(PlayerX,PlayerY,x,y):
       if(PlayerX == x and PlayerY >= y):
             direction = "Up"
       if(PlayerX == x and PlayerY <= y):
             direction = "Down"
       if(PlayerX >= x and PlayerY == y):
             direction = "Right"
       if(PlayerX <= x and PlayerY == y):
             direction = "Left"  
       return direction    
    def isinDeadZone(self,x,y):
        if(y>=self.width or x>=self.height):
            return False
        state = self.getTile(x, y)
        if(state == -1):
            return False
        elif(state[0] == '1'): 
            return True
    def isnothing(self,x,y):
        if(y>=self.width or x>=self.height):
            return False
        state = self.getTile(x, y)
        if(state == -1):
            return False
        elif(int(state)==0): 
            return True
    def stepToDeadZone(self,currentStep,x,y):
        DZSS = deadZoneStartingStep.copy()
        DZED = deadZoneExpansionDelay.copy()
        LowestDistToborder=maxStep
        for i in range(self.width):
            if( i==x or self.width-x-1==i or i==y or self.height-y-1==i):
                if i< LowestDistToborder:
                    LowestDistToborder=i
        stepToDeadZone=(DZSS +LowestDistToborder*DZED )-currentStep
        return stepToDeadZone
    
gameMap = Map(width, height)

me = Player(x, y, health)
enemy = Player(width-x, height-y, health)
stepCount = 0
log(init_msg)


def AI():
    nearestBox = gameMap.findNearestBox(me.x, me.y)
    nearestBomb = gameMap.findNearestBomb(me.x, me.y)
    nearestPowerup = gameMap.findNearestPowerup(me.x, me.y)
    
    if(nearestBomb):
        destination = gameMap.findBestPlaceForHide(nearestBomb)
        if(destination):
            me.destination = destination
            me.target = 'hide'
    elif(nearestPowerup and gameMap.findPath(me.getPos(), nearestPowerup) != None):
        me.destination = nearestPowerup
        me.target = 'placeBomb'
    elif(nearestBox):
        destination = gameMap.findBestPlaceForBomb(nearestBox)
        if(destination and gameMap.findBestPlaceForHide(destination)):
            me.destination = destination
            me.target = 'placeBomb'
        else:
            destination = gameMap.findSecondPlaceForBomb(nearestBox)
            if(destination):
                me.destination = destination
                me.target = 'placeBomb'
            else:
                me.explore()
    else:
        me.explore()
    
    me.goToDestination(gameMap)


while True:
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
    
    
    # log(gameMap.map)


    