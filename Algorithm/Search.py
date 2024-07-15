
class Search:
    def __init__(self, level):
        self.level = level


    def cannot_move(self, pos):
        return (pos[0] < 0 or pos[1] < 0 or pos[0] >= self.level.m or pos[1] >= self.level.n
                or self.level.map[pos[0]][pos[1]].value == -1)

    def creat_path(self, agent):
        current = agent.goal
        path = []
        while agent.trace[current] != agent.start:
            path.append(current)
            current = agent.trace[current]
        path.append(current)
        path.reverse()

        return path

    def run(self):
        pass
