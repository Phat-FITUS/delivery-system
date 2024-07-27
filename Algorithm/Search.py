
class Search:
    def __init__(self, level):
        self.level = level


    def cannot_move(self, pos):
        return (pos[0] < 0 or pos[1] < 0 or pos[0] >= self.level.n or pos[1] >= self.level.m
                or self.level.map[pos[0]][pos[1]].value == -1)

    def creat_path(self, agent):
        current = agent.goal
        path = []
        if agent.trace[current] is None:
            return None
        while agent.trace[current] != agent.start:
            path.append(current)
            current = agent.trace[current]
        path.append(current)
        path.reverse()

        return path
    def creat_path_2(self, expanded, trace):
        current = expanded[len(expanded) - 1]
        path = []
        if trace[current] is None:
            return None
        while trace[current] is not None:
            path.append(current)
            current = trace[current]
        path.append(current)
        path.reverse()

        return path

    def run(self):
        pass
