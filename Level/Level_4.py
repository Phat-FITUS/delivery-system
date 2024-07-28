from Algorithm.Astar.astar import Astar
from Level.Level import Level
import math
from .Level_Base import Level_Base

class Level_4(Level):
    def __init__(self, file_path):
        super().__init__(file_path)
    def count_walls(self, start, end):
        count_1 = 0
        walls_1 = dict()
        walls_1["row"] = []
        walls_1["col"] = []
        for col in self.walls["row"][start[0]]:
            if start[1] >= col and col >= end[1]:
                count_1 += 1
                walls_1["row"].append((start[0], col))
            elif col >= start[1] and col <= end[1]:
                count_1 += 1
                walls_1["row"].append((start[0], col))
        for row in self.walls["col"][end[1]]:
            if start[0] >= row and row >= end[0]:
                count_1 += 1
                walls_1["col"].append((row, end[1]))
            elif row >= start[0] and row <= end[0]:
                count_1 += 1
                walls_1["col"].append((row, end[1]))
        count_2 = 0
        walls_2 = dict()
        walls_2["row"] = []
        walls_2["col"] = []
        for col in self.walls["row"][end[0]]:
            if start[1] >= col and col >= end[1]:
                count_2 += 1
                walls_2["row"].append((end[0], col))
            elif col >= start[1] and col <= end[1]:
                count_2 += 1
                walls_2["row"].append((end[0], col))
        for row in self.walls["col"][start[1]]:
            if start[0] >= row and row >= end[0]:
                count_2 += 1
                walls_2["col"].append((row, start[1]))
            elif row >= start[0] and row <= end[0]:
                count_2 += 1
                walls_2["col"].append((row, start[1]))
        return min(count_1, count_2)

    def heuristic(self, pos, agent, save, goal_id, use_search=False):
        used = False
        if self.t - save["time"][pos] < abs(pos[0] - agent.goal[goal_id][0]) + abs(pos[1] - agent.goal[goal_id][1]):
            return (used, float("inf"))
        distance = 0
        if self.f - save["fuel"][pos] < abs(pos[0] - agent.goal[goal_id][0]) + abs(pos[1] - agent.goal[goal_id][1]):
            nearest = float("inf")
            nearest_station = None
            for station in self.fuels:
                distance = (abs(pos[0] - station[0]) + abs(pos[1] - station[1]) + self.fuels[station] +
                                    abs(agent.goal[goal_id][0] - station[0]) + abs(agent.goal[goal_id][1] - station[1]))
                # print(save["fuel"][pos])
                if (abs(pos[0] - station[0]) + abs(pos[1] - station[1])) > self.f - save["fuel"][pos] or self.t - save["time"][pos] < distance:
                    continue
                if distance < nearest:
                    nearest = distance
                    nearest_station = station
            distance = nearest
        else:
            distance = abs(pos[0] - agent.goal[goal_id][0]) + abs(pos[1] - agent.goal[goal_id][1])
            if use_search and self.count_walls(pos, agent.goal[goal_id]) and distance < 5 and save["time"][pos] >= self.t//3 and save["fuel"][pos] >= self.f//2:
                level = Level_Base()
                level.agents = dict()
                used = True
                level.copy(self.map, self.m, self.n, self.t, self.f, agent, self.walls, self.fuels)
                level.agents[0].goal = [agent.goal[goal_id]]
                algo = Astar(level)
                solve = algo.run(save["time"][pos], save["fuel"][pos])
                if solve is not None:
                    distance = len(solve)-2
                else:
                    distance = float("inf")
        if distance > self.t - save["time"][pos]:
            return (used, float("inf"))
        for i in range(goal_id+1, len(agent.goal)):
            distance += abs(agent.goal[i-1][0] - agent.goal[i][0]) + abs(agent.goal[i-1][1] - agent.goal[i][1])
        heuristic = pow(distance, 2)
        return (used, heuristic)
