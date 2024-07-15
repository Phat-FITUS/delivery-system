from Level.Level import Level


class Level_1(Level):
    def __init__(self, file_path):
        super().__init__(file_path)

    def heuristic(self, pos, goal, agent):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
