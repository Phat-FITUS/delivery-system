from random import randint


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
        self.goal = goal  # (x, y)
        self.id = id
        self.frontier = None
        self.trace = None
        self.expanded = None
        self.cost = None
        self.eval = None
        self.time = None
        self.fuel = None

    def generate_goal(self, level):
        valid_pos = []
        for i in range(level.n):
            for j in range(level.m):
                if level.map[i][j].value > 0 and level.map[i][j].agent is False:
                    valid_pos.append((i, j))
        new_pos = valid_pos[randint(0, len(valid_pos) - 1)]
        self.goal = new_pos


MoveDirection = {
    "up": (1, 0),
    "down": (-1, 0),
    "left": (0, -1),
    "right": (0, 1),
}
