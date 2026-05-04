import random
import numpy as np

import gridworld as gw

class Agent:
    exampleValue = {"<hash>":["opt1 value", "opt2 value"],
                    "abc123": [12.53, -2.04, 3.71]}

    def __init__(self, animal: gw.Animal, agent: Agent = None):
        self.animal = animal
        animal.agent = self

        self.value = {}
        self.valueCnt = {}
        self.epsilon = 0.10
        self.r = 2
        self.initValue = 100
        self.history = []

        # clone the mind of the prev 
        if agent != None:
            self.value = agent.value
            self.valueCnt = agent.valueCnt

    def addHistory(self, action: int, state: str):
        self.history.append({state: action})

    # Uses the agent to pick an action. This function does not calculate reward or update value function.
    def getAction(self, state):
        state = str(state)
        if state not in self.value.keys():
            initValuesAtState(self, state)

        # Pick option with highest value function (Exploit)
        action = argmax(self.value[str(state)])

        n = self.valueCnt[state][action]
        if n > 20:
            epsilon = 0.1
        else:
            epsilon = self.epsilon

        if random.random() <= epsilon:
            # Pick random choice (Explore)
            action = random.choice(Action.options)

        self.addHistory(action, state)
        return action

    def reward(self, reward: int):
        # go through each action in the history
        for i in range(len(self.history)):
            d = self.history[i]

            # update the rolling average of the value function for that action
            state = list(d.keys())[0]
            action = d[state]

            avg = self.value[state][action]
            n = self.valueCnt[state][action] # get the number of times you've updated this action

            n += 1
            # 'thisReward' is the reward for this particular action
            # the propogation of value increase for  an action more recent 
            # to a reward signal should be increased more.
            thisReward = reward / (len(self.history) - i)
            avg += (thisReward - avg) / n # rolling avg calculation
            # update the new value function and 'n' for rolling avg
            self.value[state][action] = avg
            self.valueCnt[state][action] = n
        # clear the history
        self.history = []

class Action:
    options = range(0, 3+1)
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

trainingNum = 10**6

# Returns the index of the highest value, breaking ties RANDOMLY
def argmax(arr: list):
    max = None
    maxIndex = None
    for i in range(len(arr)):
        item = arr[i]

        # Don't allow for string inputs
        if type(item) == str:
            return None

        # check if 'item' can be cast as a float
        try:
            item = float(item)
        except:
            # Error: incompatible types in the list
            return None

        # keep track of the highest value so far
        if max == None or item > max:
            max = item
            maxIndex = i

    # check for ties, pick a random one among them
    if arr.count(max) > 1:
        # find the index of each tie value
        indexes = []
        for i in range(len(arr)):
            if arr[i] == max:
                indexes.append(i)
        # pick a random one of the ties
        maxIndex = random.choice(indexes)

    # return the index of the max value (or a random one of the ties) 
    return maxIndex
        

def initValuesAtState(agent: Agent, state):
    arr = []
    arrCnt = []
    # set initial values for the value function at the given state
    for i in Action.options:
        arr.append(agent.initValue)
        arrCnt.append(0) # n starts at zero
    agent.value[str(state)] = arr
    agent.valueCnt[str(state)] = arrCnt


def main():
    # create N agents
    N = 1

    # create the gridworld
    animals = gw.initGridworld(30, 20, N)

    agents = []
    for i in range(N):
        agents.append(Agent(animals[i]))

    # loop (rounds)
    roundNum = 0
    while True:

        if roundNum > 0 and roundNum % 10 == 0:
            gw.spawnFood(10)

        # for each agent
        actions = {}
        for a in agents:
            # kill agents which have no energy left
            if a.animal.energy <= 0 and len(agents) > 1:
                print("KILLING AGENT")
                agents.remove(a)
                gw.setWorld(a.animal.x, a.animal.y, gw.Symbol.MEAT)
                gw.animals.remove(a.animal)
                continue

            # get the action for the agent
            state = gw.getAnimalVision(a.animal, a.r)
            action = a.getAction(state)
            if action == None:
                print(f"Why is action None??? (animal id = {a.animal.id})")
            actions[a] = action
        # for each action that needs to be applied
        for agent in actions.keys():
            act = actions[agent]
            # apply the actions to the world
            dx, dy = 0, 0
            match act:
                case Action.UP:
                    dy = 1
                case Action.RIGHT:
                    dx = 1
                case Action.DOWN:
                    dy = -1
                case Action.LEFT:
                    dx = -1


            # Apply the action
            gw.moveAnimal(agent.animal, dx, dy)
            # I believe the reward/value updates would happen here? Or idk.
            # This is likely going to be a continuous (non-episodic) agent, so it's kinda weird yk
            # I suppose more likely is that we keep track of actions taken for each agent, then when we
            # actually achieve something good or bad, then we doll out rewards (e.g. food or pain).

            # Spawn a new child when the parent eats enough food
            childX, childY = agent.animal.x+1, agent.animal.y+1
            if agent.animal.energy > 100 and gw.getWorld(childX, childY) == None:
                print("CREATING OFFSPRING")
                # create the child
                child = gw.Animal(childX, childY, len(gw.animals) % 10)
                # place it into the world
                gw.animals.append(child)
                gw.setWorld(childX, childY, gw.Symbol.ANIMAL)
                #assign an agent to the animal
                agents.append(Agent(child, agent))
                # reduce the food
                agent.animal.energy -= 50
        if roundNum > trainingNum:
            gw.printWorld()
            a = agents[0]
            gw.printVision(gw.getAnimalVision(a.animal, a.r), a.animal.x, a.animal.y, a.r)
            input("Press enter to continue\n")
        roundNum += 1
        print(roundNum)




if __name__ == "__main__":
    trainingNum = int(input("Enter training rounds:\n> "))
    main()