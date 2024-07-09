from Level.Level import Level


class Level_1(Level):
    def __init__(self, file_path):
        super().__init__(file_path)

    def heuristic(self, pos, goal, current=None):
        return abs(pos[0] - goal.pos[0]) + abs(pos[1] - goal.pos[1])
