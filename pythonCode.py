#region VEXcode Generated Robot Configuration
import math
import random
from vexcode_vr import *

# Brain should be defined by default
brain=Brain()

drivetrain = Drivetrain("drivetrain", 0)
pen = Pen("pen", 8)
pen.set_pen_width(THIN)
left_bumper = Bumper("leftBumper", 2)
right_bumper = Bumper("rightBumper", 3)
front_eye = EyeSensor("frontEye", 4)
down_eye = EyeSensor("downEye", 5)
front_distance = Distance("frontdistance", 6)
distance = front_distance
magnet = Electromagnet("magnet", 7)
location = Location("location", 9)

#endregion VEXcode Generated Robot Configuration
from vexcode_vr import *


#8x8 2d array, 0 marks unvisited, 1 marks visited and 2 marks target square
maze = [[0 for _ in range(8)] for _ in range(8)] 
path = []
walls = {} #dictionary to map each cell to its wall directions
startPosition = None

def convertToGrid(coords):
    """
    Convert maze coordinates from millimeters to grid cell coordinates
    so it can be printed to the console easier.
    Takes in a tuple of x and y coordinates in MM
    Returns a tuple of row and column grid coordinates from 0 to 7
    """
    row = int((coords[1] + 1000) / 250)
    col = int((coords[0] + 1000) / 250)
    return (row, col)


def mapMaze():
    """
    Maps the entire maze using Depth-first search with backtracking and pruning
    at the same time.
    Appends the unoptimized path to the path global variable.
    marks the visited cells as 1 in the global maze 2d array.

    """
    global startPosition
    stack = [] #stack for backtracking
    endReached = False #when this is True, no longer append to path
    startPosition = convertToGrid((location.position(X, MM), location.position(Y, MM)))
    while True:
        wait(5, MSEC)
        coord = (location.position(X, MM), location.position(Y, MM))
        converted = convertToGrid(coord)
        #append this cell to the path only until end is reached
        if not endReached:
            path.append(converted)
        row, col = converted[0], converted[1]
        maze[row][col] = 1 #mark cell as visited

        if down_eye.detect(RED):
            maze[row][col] = 2 #mark as end square
            endReached = True
        #check the next univisted square
        nextSquare = find_unvisited(row, col)
        if nextSquare:
            #append current position to the stack and move robot to the next unvisited cell.
            stack.append((row, col))
            moveToCell(nextSquare)
        elif len(stack) > 0:
            #backtrack to the previous square, since there are no unvisited adjacent cells.
            prevSquare = stack.pop()
            moveToCell(prevSquare)
        else:
            break
        



def find_unvisited(row, col):
    """
    Find the next unvisited neighbouring cell and detect walls
    Takes row and col of the current position
    Returns a tuple of row and col of the unvisited neighbor
    """
    #coordinate increment based on the direction
    direction = {
        0: (1, 0),
        90: (0, 1),
        180: (-1, 0),
        270: (0, -1)
    }
    #initialise walls for this cell if not already done
    if (row, col) not in walls:
        walls[(row, col)] = set()
    #check all directions, starting from North
    for angle in [0, 90, 180, 270]:
        r, c = direction[angle]
        newR, newC = row + r ,col + c

        #check boundaries
        if 0 <= newR < 8 and 0 <= newC < 8:
            drivetrain.turn_to_heading(angle, DEGREES)
            #check walls
            if front_distance.get_distance(MM) <= 250:
                walls[(row, col)].add(angle)
            else:
                #check if visited
                if maze[newR][newC] == 0:
                    return (newR, newC)
        else:
            #out of bounds also counts as a wall
            walls[(row, col)].add(angle)
    return None

def moveToCell(coords):
    """
    Move the robot to an adjacent cell
    Takes a tuple containing the row and column of the target cell.
    """
    cRow, cCol = convertToGrid((location.position(X, MM), location.position(Y, MM)))
    targetRow = coords[0]
    targetCol = coords[1]
    #determine which direction to face based on the target square relative to current position
    if targetRow > cRow:
        angle = 0
    elif targetRow < cRow:
        angle = 180
    elif targetCol > cCol:
        angle = 90
    elif targetCol < cCol:
        angle = 270
    else:
        return

    drivetrain.turn_to_heading(angle, DEGREES)
    drivetrain.drive_for(FORWARD, 250, MM)


def optimizePath():
    """
    Remove dead ends from the path to create the single optimal path

    when a cell is seen for the first time, add it to the stack and the set
    when it is seen again in the set, pop all cells back to the first time it was seen.

    Returns a list of coordinates representing the optimal path.
    """
    stack = []
    #we use a set here for O(1) lookup time, rather than having to iterate through 
    #the stack everytime
    seen = set() 
    for coord in path:
        if coord not in seen:
            stack.append(coord)
            seen.add(coord)
        elif coord in seen:
            #cell has been revisited, remove the dead end by popping back to first instance
            while stack and stack[-1] != coord:
                seen.remove(stack.pop())
    return stack

def walkOptimalPath(optimized):
    """
    Walk the optimal path, paving the path with a green pen.
    """
    pen.move(DOWN)
    pen.set_pen_color(GREEN)
    for i in range(1, len(optimized)):
        moveToCell(optimized[i])


def printMaze():
    """
    prints an ASCII-style maze to the console
    """
    brain.print("\n Maze \n")

    #Python arrays start from 0 and go down to 7
    #But the maze has 0 at the bottom and 7 at the top.
    #So iterate backwards.
    for row in range(7, -1, -1):
        #print the top border for horizontal walls
        topLine = ""
        for col in range(8):
            topLine += "+"
            #check if there's a wall north of the cell
            if (row, col) in walls and 0 in walls[(row, col)]:
                topLine += "---"
            else:
                topLine += "   "
        topLine += "+"
        brain.print(topLine + "\n")

        cellLine = ""
        for col in range(8):
            if (row, col) in walls and 270 in walls[(row, col)]:
                cellLine += "|"
            else:
                cellLine += " "
        
            if startPosition and (row, col) == startPosition:
                cellLine += " S "
            elif maze[row][col] == 2:
                cellLine += " E "
            elif maze[row][col] == 1:
                cellLine += "   "
            else:
                cellLine += "   "

        if (row, 7) in walls and 90 in walls[(row, 7)]:
            cellLine += "|"
        else:
            cellLine += " "
        brain.print(cellLine + "\n")

    bottomLine = ""
    for col in range(8):
        bottomLine += "+"
        if (0, col) in walls and 180 in walls[(0, col)]:
            bottomLine += "---"
        else:
            bottomLine += "   "
    bottomLine += "+"
    brain.print(bottomLine + "\n")

def when_started1():
    #set the robot to max speed for a faster runtime
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(100, PERCENT)

    mapMaze()
    printMaze()
    optimized = optimizePath()

    brain.print("Optimized path: \n")
    brain.print(path)

    walkOptimalPath(optimized)





vr_thread(when_started1)
