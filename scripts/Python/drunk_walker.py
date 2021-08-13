import numpy as np
from uuid import uuid4

'''
Notes I have found:

Modifying the number of walkers change the layouts:
- less max walkers make more corridors
- more max walkers make larger open spaces
'''

# Globals
FLOOR = '.'
WALL = '*'
EMPTY = ' '
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
WIDTH = 100
HEIGHT = 30
X_BOUNDS = [2, WIDTH-2]
Y_BOUNDS = [2, HEIGHT-2]
X_START = int((X_BOUNDS[1] + X_BOUNDS[0]) / 2)
Y_START = int((Y_BOUNDS[1] + Y_BOUNDS[0]) / 2)
SPAWN_CHANCE = KILL_CHANCE = .20
DIR_CHANGE_CHANCE = .55
FILL_REQ = int(.10 * WIDTH * HEIGHT)
MAX_ITERS = 10000
MAX_WALKERS = 5


class Walker():
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def walk(self):
        # Check if we need to change direction
        if(np.random.rand() <= DIR_CHANGE_CHANCE):
            self.direction = np.random.randint(UP, LEFT+1)

        if(self.direction is UP):
            if(self.y - 1 >= Y_BOUNDS[0]):
                self.y -= 1
            else:
                self.direction = np.random.randint(UP, LEFT+1)
        if(self.direction is RIGHT):
            if(self.x + 1 <= X_BOUNDS[1]):
                self.x += 1
            else:
                self.direction = np.random.randint(UP, LEFT+1)
        if(self.direction is DOWN):
            if(self.y + 1 <= Y_BOUNDS[1]):
                self.y += 1
            else:
                self.direction = np.random.randint(UP, LEFT+1)
        if(self.direction is RIGHT):
            if(self.x - 1 <= X_BOUNDS[0]):
                self.x -= 1
            else:
                self.direction = np.random.randint(UP, LEFT+1)

    def get_pos(self):
        return [self.x, self.y]

def make_map(width, height):
    # Print Map ID
    print('Map {}\n'.format(str(uuid4())))

    # Do setup
    grid = np.full((WIDTH, HEIGHT), EMPTY)
    walkers = []
    walkers.append(Walker(X_START, Y_START, np.random.randint(UP, LEFT+1)))
    total_filled = 0
    iters = 0
    loop = True


    # Let walkers walk!
    while(loop and iters <= MAX_ITERS):

        # Loop through walkers and place floor
        for walker in walkers:
            if(grid[walker.x][walker.y] == EMPTY):
                total_filled += 1
            grid[walker.x][walker.y] = FLOOR

        # Now check to destroy walkers, only 1 per iteration
        if(len(walkers) > 1):
            for walker in walkers:
                if(np.random.rand() <= KILL_CHANCE):
                    walkers.remove(walker)
                    break

        # Now try to spawn walkers, one per iteration
        for walker in walkers:
            if(np.random.rand() <= SPAWN_CHANCE):
                if(len(walkers) <= MAX_WALKERS):
                    walkers.append(Walker(walker.x, walker.y, np.random.randint(UP, LEFT+1)))

        # Now walk the walkers
        for walker in walkers:
            walker.walk()

        # Check if we need to continue looping
        iters += 1
        if(total_filled >= FILL_REQ):
            loop = False

    # Now do walls
    for row in range(HEIGHT):
        for col in range(WIDTH):
            # If this space is empty, check if it is next to a floor.
            # if so, make this a wall
            plus_x_in = False
            plus_y_in = False
            minus_x_in = False
            minus_y_in = False

            if(grid[col][row] == EMPTY):
                if(row + 1 < HEIGHT):
                    plus_y_in = True
                    if(grid[col][row+1] == FLOOR):
                        grid[col][row] = WALL

                if(col + 1 < WIDTH):
                    plus_x_in = True
                    if(grid[col+1][row] == FLOOR):
                        grid[col][row] = WALL

                if(row - 1):
                    minus_y_in = True
                    if(grid[col][row-1] == FLOOR):
                        grid[col][row] = WALL
                
                if(col - 1):
                    minus_x_in = True
                    if(grid[col-1][row] == FLOOR):
                        grid[col][row] = WALL

                if(plus_x_in and plus_y_in):
                    if(grid[col+1][row+1] == FLOOR):
                        grid[col][row] = WALL

                if(minus_x_in and minus_y_in):
                    if(grid[col-1][row-1] == FLOOR):
                        grid[col][row] = WALL

                if(plus_x_in and minus_y_in):
                    if(grid[col+1][row-1] == FLOOR):
                        grid[col][row] = WALL

                if(minus_x_in and plus_y_in):
                    if(grid[col-1][row+1] == FLOOR):
                        grid[col][row] = WALL

    # Print the map
    grid = grid.T
    for col in grid:
        print(''.join(col))

    # DONE!


def main():
    while(True):
        make_map(WIDTH, HEIGHT)
        print('\n')
        input("Press Enter to generate new map...")

if __name__ == '__main__':
    main()