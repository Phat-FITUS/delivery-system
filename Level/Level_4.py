from Level.Level import Level
import math


class Level_4(Level):
    def __init__(self, file_path):
        super().__init__(file_path)
    def count_walls(self, start, end):
        count_1 = 0
        walls_1 = []
        for col in self.walls["row"][start[0]]:
            if start[1] >= col and col >= end[1]:
                count_1 += 1
                walls_1.append((start[0], col))
            elif col >= start[1] and col <= end[1]:
                count_1 += 1
                walls_1.append((start[0], col))
        for row in self.walls["col"][end[1]]:
            if start[0] >= col and col >= end[0]:
                count_1 += 1
            elif col >= start[0] and col <= end[0]:
                count_1 += 1
        count_2 = 0
        for col in self.walls["row"][end[0]]:
            if start[1] >= col and col >= end[1]:
                count_2 += 1
            elif col >= start[1] and col <= end[1]:
                count_2 += 1
        for row in self.walls["col"][start[1]]:
            if start[0] >= row and row >= end[0]:
                count_2 += 1
            elif row >= start[0] and row <= end[0]:
                count_2 += 1
        return max(count_1, count_2)
    def compute_distance(self, point1, point2):
        number_of_wall = self.count_walls()

    def heuristic(self, pos, agent, save, goal_id, state):

        if self.t - save["time"][pos] < abs(pos[0] - agent.goal[goal_id][0]) + abs(pos[1] - agent.goal[goal_id][1]):
            return float("inf")
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
            # if nearest_station is not None:

            distance = nearest
        else:
            distance += abs(pos[0] - agent.goal[goal_id][0]) + abs(pos[1] - agent.goal[goal_id][1])
        for i in range(goal_id+1, len(agent.goal)):
            distance += abs(agent.goal[i-1][0] - agent.goal[i][0]) + abs(agent.goal[i-1][1] - agent.goal[i][1])
        heuristic = distance
        return heuristic
