import random

class animal:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id


world = [] # options {animal 0, food 1, wall 2}
worldX = None
worldY = None
animals = []

def getWorld(x, y):
    return world[y][x]

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
                    print(f"\nx = {x}, y = {y}\nanimals: {animals}")
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

def initGridworld(sizeX, sizeY, organismCnt):
    global worldX, worldY, animals
    worldX = sizeX
    worldY = sizeY
    # initialize empty gridworld
    initWorld(sizeX, sizeY)

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
        animals.append(animal(x, y, i))
        setWorld(x, y, 0) # 0: animal

    # spawn food
    foodCnt = 20
    for i in range(foodCnt):
        x, y = 0, 0
        flag = True
        # pick empty x,y coords
        while(flag or getWorld(x,y) != None):
            flag = False
            x = random.randrange(sizeX)
            y = random.randrange(sizeY)
        # place the food
        setWorld(x, y, 1) # 1: food

    print("Gridworld intialized:")
    printWorld()
    return animals

# transform an animal by dx, dy, unless there is something in its destination, then do nothing.
def moveAnimal(animal, dx, dy):
    global world

    x = animal.x
    y = animal.y

    if setWorld(x+dx, y+dy, 0, overwrite=False) == None:
        # Error
        return None
    setWorld(animal.x, animal.y, None)
    animal.x += dx
    animal.y += dy


# MAIN()

initGridworld(30, 30, 5)

moveAnimal(animals[0], 1, 1)
printWorld()