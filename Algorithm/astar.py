from Global.DataStructure import Frontier
from .Search import *
from Global.variable import *


class Astar(Search):
    def __init__(self, level, heuristic):
        super().__init__(level)
        self.time = dict()
        self.fuel = dict()

    def run(self):
        self.frontier = Frontier()
        self.frontier.put((0, self.level.start.pos))
        self.expanded = []
        self.trace = dict()
        cost = dict()
        eval = dict()
        self.time = dict()
        self.fuel = dict()

        while not self.frontier.empty():
            current = self.frontier.get()

            if current == self.level.goal.pos:
                break

            if current == self.level.start.pos:
                self.trace[self.level.start], cost[self.level.start], eval[self.level.start] = None, 0, 0
            self.expanded.append(current)

            for move in MoveDirection.values():
                next_pos = (current.pos[0] + move[0], current.pos[1] + move[1])
                if self.out_map(next_pos):
                    continue

                eval_score = cost[current] + 1 + self.level.heuristic(next_pos, self.level.goal, current)

                if next_pos not in self.expanded:
                    eval[next_pos] = eval_score
                    self.frontier.put((eval_score, next_pos))
                    self.trace[next_pos] = current
                    cost[next_pos] = cost[current] + 1
                    self.time[next_pos] = self.time[current] + 1 + self.level.map[current[0]][current[1]].value
                    self.fuel[next_pos] = self.fuel[current] + 1 + self.level.map[current[0]][current[1]].fuel
        return self.creat_path()