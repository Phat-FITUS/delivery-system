from random import randint
from Global.DataStructure import *

class Position:
    def __init__(self, x, y, value=0, fuel=0, agent=False):
        self.pos = (x, y)
        # Value is time
        self.value = value
        self.fuel = fuel
        self.agent = agent


class Agent:
    def __init__(self, start=None, goal=None, id=0):
        self.start = start  # (x,y)
        if goal is None:
            self.goal = []
        else:
            self.goal = [goal] # (x, y)
        print("==============----------=============")
        print(self.goal)
        self.id = id
        self.current = None

    def generate_goal(self, state, level):
        valid_pos = []
        for i in range(level.n):
            for j in range(level.m):
                same = False
                for pos in state:
                    if pos == (i, j):
                        same = True
                        break
                if same:
                    continue
                if level.map[i][j].value >= 0:
                    valid_pos.append((i, j))
        new_pos = valid_pos[randint(0, len(valid_pos) - 1)]
        self.start = self.goal
        self.goal.append(new_pos)


MoveDirection = {
    "down": (1, 0),
    "up": (-1, 0),
    "left": (0, -1),
    "right": (0, 1),
    "wait": (0, 0),
}
