from Global.variable import *

class Level:
    def __init__(self, file_path):
        self.load(file_path)

    def load(self, file_name):
        # Load to initial variables
        # Map is a matrix of Position
        self.map = None
        self.n = 0
        self.m = 0
        # Start and Goal are a Position
        self.start = None
        self.goal = None

        self.other_start = None
        self.other_goal = None

    def heuristic(self, pos, goal, current=None):
        pass
