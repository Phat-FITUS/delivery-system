
class Search:
    def __init__(self, level):
        self.level = level
        self.current = level.start
        self.movement = level.start
        self.frontier = None
        self.expanded = None
        self.trace = None

    def cannot_move(self, pos):
        return (pos[0] < 0 or pos[1] < 0 or pos[0] >= self.level.m or pos[1] >= self.level.n
                or self.level.map[pos[0]][pos[1]].value == -1)

    def creat_path(self):
        current = self.level.goal.pos
        path = []
        while self.trace[current] != self.level.start.pos:
            path.append(current)
            current = self.trace[current]
        path.append(current)
        path.reverse()

        return path

    def run(self):
        pass
