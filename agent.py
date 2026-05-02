import random
import numpy as np

import gridworld as gw

class Agent:
    exampleValue = {"<hash>":["opt1 value", "opt2 value"],
                    "abc123": [12.53, -2.04, 3.71]}

    def __init__(self, animal: gw.Animal):
        self.animal = animal
        animal.agent = self

        self.value = {}
        self.valueCnt = {}
        self.epsilon = 0.10
        self.r = 2
        self.initValue = 100
        self.history = []

    def addHistory(self, action: int, state: str):
        self.history.append({state: action})

    # Uses the agent to pick an action. This function does not calculate reward or update value function.
    def getAction(self, state):
        state = str(state)
        if state not in self.value.keys():
            initValuesAtState(self, state)

        # Pick option with highest value function (Exploit)
        action = np.argmax(self.value[str(state)])

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
        print(f"Reward for animal {self.animal.id}!!")
        # go through each action in the history
        for d in self.history:
        # update the rolling average of the value function for that action
            state = list(d.keys())[0]
            action = d[state]

            avg = self.value[state][action]
            n = self.valueCnt[state][action] # get the number of times you've updated this action
            print(f"n = {n}")

            n += 1
            avg += (reward - avg) / n # rolling avg calculation
            self.value[state][action] = avg
        # clear the history
        self.history = []

class Action:
    options = range(0, 3+1)
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

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
    # create the gridworld
    animals = gw.initGridworld(30, 30, 3)

    # create N agents
    N = 3
    agents = []
    for i in range(N):
        agents.append(Agent(animals[i]))

    # loop (rounds)
    roundNum = 0
    while True:

        if roundNum > 0 and roundNum % 10 == 0:
            gw.spawnFood(2)

        # for each agent
        actions = {}
        for a in agents:
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
            # bodge fix to make them NOT GO DOWN
            if act != Action.DOWN:
                agent.reward(1)


            # Apply the action
            gw.moveAnimal(agent.animal, dx, dy)
            # I believe the reward/value updates would happen here? Or idk.
            # This is likely going to be a continuous (non-episodic) agent, so it's kinda weird yk
            # I suppose more likely is that we keep track of actions taken for each agent, then when we
            # actually achieve something good or bad, then we doll out rewards (e.g. food or pain).
        if roundNum > 10**4:
            gw.printWorld()
            input("Press enter to continue\n")
        roundNum += 1
        print(roundNum)




if __name__ == "__main__":
    main()