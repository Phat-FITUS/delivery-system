from Level.Level import Level
import math

class Level_2(Level):
    def __init__(self, file_path):
        super().__init__(file_path)

    def heuristic(self, pos, agent, level):

        return abs(pos[0] - agent.goal[0]) + abs(pos[1] - agent.goal[1])
