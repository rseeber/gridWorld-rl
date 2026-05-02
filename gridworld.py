import random

class Animal:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.energy = 10
        self.agent = None

class Symbol:
    EMPTY = None
    ANIMAL = 0
    FOOD = 1
    WALL = 2

    HIDDEN = -1
    OUT_OF_BOUNDS = -2


world = [] # options {animal 0, food 1, wall 2}
worldX = None
worldY = None
animals = []

def getWorld(x, y):
    try:
        val = world[y][x]
    except IndexError:
        val = Symbol.OUT_OF_BOUNDS # -2: Out of bounds
    return val


def setWorld(x, y, value, overwrite=True):
    global world
    if not overwrite and world[y][x] != None:
        return None
    world[y][x] = value
    return value

def initWorld(sizeX, sizeY, homogValue=None):
    global world

    for y in range(sizeY):
        world.append([])
        for x in range(sizeX):
            world[y].append(homogValue)

def printVision(arr, centerX, centerY, r):
    convert = {Symbol.EMPTY: "_", 
               Symbol.ANIMAL: "A", 
               Symbol.FOOD: "*", 
               Symbol.WALL: "#", 
               Symbol.HIDDEN: "?"}
    # iterate through each x, y tile
    for y in range(len(arr)):
        for x in range(len(arr[y])):
            # get the value at that tile
            val = arr[y][x]
            globalX = x + centerX - r
            globalY = y + centerY - r
            # print the id if it's an animal
            if val == Symbol.ANIMAL:
                val = findAnimal(globalX, globalY).id
            else:
                # use the conversion table
                val = convert[val]
            print(f"{val} ", end="")
        print()
    print("\n")

def printWorld():
    convert = {None: "_", 0: "A", 1: "*", 2: "#"}
    # iterate through each x, y tile
    for y in range(worldY):
        for x in range(worldX):
            # get the value at that tile
            val = getWorld(x,y)
            # if it's an animal, represent it by its id
            if val == 0: 
                try:
                    val = findAnimal(x, y).id
                except:
                    print(f"\ncouldn't find animal at x = {x}, y = {y}\nanimals: {animals}")
            # otherwise, use the conversion table
            else:
                val = convert[val]
            print(f"{val} ", end="")
        print()
    print("\n")
    
# return the animal located at the coordinates
def findAnimal(x, y):
    for a in animals:
        if a.x == x and a.y == y:
            return a

# return the animal with the given id
def findAnimal_id(id):
    for a in animals:
        if a.id == id:
            return a

def getAnimalVision(animal, r):
    vision = []
    # Recall that "x^2 + y^2 < r^2" means that (x,y) is inside of the circle with radius r (centered at the origin)
    r2 = r * r
    # iterate through all tiles in a square with radius r around the animal
    for y in range(2*r + 1):
        vision.append([])
        for x in range(2*r + 1):
            # check if the tile is within a circle of radius r
            lhs = (x-r)**2 + (y-r)**2
            if (x-r)**2 + (y-r)**2 <= r2:
                # include the tile
                vision[y].append(getWorld(x-r+animal.x, y-r+animal.y))
            else:
                vision[y].append(-1) # -1: hidden tile
    return vision
            


def initGridworld(sizeX, sizeY, organismCnt):
    global worldX, worldY, animals
    worldX = sizeX
    worldY = sizeY
    # initialize empty gridworld
    initWorld(sizeX, sizeY)

    # setup playground walls
    # Top and bottom walls
    for i in range(worldX):
        setWorld(i, 0, Symbol.WALL)
        setWorld(i, worldY-1, Symbol.WALL)
    # Left and right walls
    for i in range(worldY):
        setWorld(0, i, Symbol.WALL)
        setWorld(worldX-1, i, Symbol.WALL)
    

    # setup the animals
    animals = []
    for i in range(organismCnt):
        flag = True
        x, y = 0, 0
        # pick empty x,y coords
        while(flag or getWorld(x, y) != None):
            flag = False
            x = round(random.gauss(sizeX/2))
            y = round(random.gauss(sizeY/2))
        animals.append(Animal(x, y, i))
        setWorld(x, y, 0) # 0: animal

    # spawn food
    spawnFood(20)
    # also for now, just spawn some food at the bottom row
    for i in range(worldX):
        setWorld(i, worldY-2, Symbol.FOOD, overwrite=False)

    print("Gridworld intialized:")
    printWorld()
    return animals

def spawnFood(foodCnt):
    for i in range(foodCnt):
        x, y = 0, 0
        flag = True
        attempts = 0
        # pick empty x,y coords
        while(flag or getWorld(x,y) != None):
            flag = False
            x = random.randrange(worldX)
            y = random.randrange(worldY)
            # give up if you can't find any empty tiles
            attempts += 1
            if attempts > 10:
                return None
        # place the food
        setWorld(x, y, Symbol.FOOD) # 1: food


# transform an animal by dx, dy, unless there is something in its destination, then do nothing.
def moveAnimal(animal: Animal, dx: int, dy: int):
    global world

    x = animal.x
    y = animal.y

    newSpot = getWorld(x+dx, y+dy) 

    # Don't allow animals to move to occupied locations
    if newSpot not in [Symbol.FOOD, Symbol.EMPTY]:
        # Error
        return None

    # depleate energy when moving
    animal.energy -= 0.1

    if newSpot == Symbol.FOOD:
        animal.energy += 5
        # Is this where we should be sending the reward signal?
        if animal.agent != None:
            animal.agent.reward(1)

    # place the animal in the NEW position
    setWorld(x+dx, y+dy, 0)   
    # set the OLD position to be empty
    setWorld(animal.x, animal.y, None)
    # update coords on the Animal class object
    animal.x += dx
    animal.y += dy


# MAIN()
def main():
    random.seed(101)
    animals = initGridworld(30, 30, 5)
    a = animals[0]

    moveAnimal(a, 1, 1)
    printWorld()

    vision = getAnimalVision(a, 2)
    printVision(vision, a.x, a.y, 2)

if __name__ == "__main__":
    main()