# Homa AI competition

## 1. run
  ```
  python main.py -p1 player1.py -p2 player2.py
  ```

### 2. Output Commands
  ```
  print(0) -> Go left
  print(1) -> Go right
  print(2) -> Go up
  print(3) -> Go down
  print(4) -> Stay
  print(5) -> Place Bomb
  print(6) -> Place Trap left
  print(7) -> Place Trap right
  print(8) -> Place Trap up
  print(9) -> Place Trap down
  ```

### 3. Input data
 * If enemy is **not** in vision:
  ```
  stepCount, lastAction, x, y, health, healthUpgradeCount, bombRange, trapCount, enemyInVision, numberOfTilesInVision, [x, y, tileState]
  ```
 * If enemy is in vision:
  ```
  stepCount, lastAction, x, y, health, healthUpgradeCount, bombRange, trapCount, enemyInVision, enemyX, enemyY, numberOfTilesInVision, [x, y, tileState]
  ```
 
### 4. Tile States
  ```
  0: Tile is in dead zone
  1: Fire (explosion side effect)
  2: Box
  3: Wall
  4: Bomb
  5: Bomb range upgrade
  6: Health upgrade
  7: Trap upgrade
  8: A player
  ```
