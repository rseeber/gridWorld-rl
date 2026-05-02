import random
import numpy as np

import gridworld as gw

class Agent:
    exampleValue = {"<hash>":["opt1 value", "opt2 value"],
                    "abc123": [12.53, -2.04, 3.71]}

    def __init__(self, animal):
        self.animal = animal
        self.value = {}
        self.epsilon = 0.50
        self.r = 2
        self.initValue = 0

class Action:
    options = range(0, 3+1)
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

def initAgent():
    # initialize the value function
    pass

def initValuesAtState(agent: Agent, state):
    arr = []
    # set initial values for the value function at the given state
    for i in Action.options:
        arr.append(agent.initValue)
    agent.value[str(state)] = arr

# Uses the agent to pick an action. This function does not calculate reward or update value function.
def getAgentAction(agent: Agent, state):
    state = str(state)
    if state not in agent.value.keys():
        initValuesAtState(agent, state)

    action = None
    if random.random() <= agent.epsilon:
        # Pick random choice (Explore)
        action = random.choice(Action.options)
    else:
        # Pick option with highest value function (Exploit)
        action = np.argmax(agent.value[str(state)])
    return action

def main():
    # create the gridworld
    animals = gw.initGridworld(30, 30, 3)

    # create N agents
    N = 3
    agents = []
    for i in range(N):
        agents.append(Agent(animals[i]))

    # loop (rounds)
    while True:
        # for each agent
        actions = {}
        for a in agents:
            # get the action for the agent
            state = gw.getAnimalVision(a.animal, a.r)
            action = getAgentAction(a, state)
            if action == None:
                print(f"Why is action None??? (animal id = {a.animal.id})")
            actions[a] = action
            print(f"Action {action} for agent {a.animal.id}")
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
        gw.printWorld()
        input("Press enter to continue\n")




if __name__ == "__main__":
    main()