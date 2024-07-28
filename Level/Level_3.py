from Level.Level import Level
import math


class Level_3(Level):
    def __init__(self, file_path):
        super().__init__(file_path)

    def heuristic(self, pos, agent, save, goal_id, state):
        distance = 0
        if self.f - save["fuel"][pos] < abs(pos[0] - agent.goal[goal_id][0]) + abs(
                pos[1] - agent.goal[goal_id][1]):
            nearest = float("inf")
            for station in self.fuels:
                # print("bafdjhefbjhrejhghe")
                # print(pos)
                # print(station)
                # print(agent.goal[i][i])
                distance = (abs(pos[0] - station[0]) + abs(pos[1] - station[1]) + self.fuels[station] +
                            abs(agent.goal[goal_id][0] - station[0]) + abs(agent.goal[goal_id][1] - station[1]))
                # print(save["fuel"][pos])
                if (abs(pos[0] - station[0]) + abs(pos[1] - station[1])) > self.f - save["fuel"][pos] - 1:
                    continue
                if distance < nearest:
                    nearest = distance
            distance = nearest
        else:
            distance += abs(pos[0] - agent.goal[goal_id][0]) + abs(pos[1] - agent.goal[goal_id][1])
        for i in range(goal_id + 1, len(agent.goal)):
            distance += abs(pos[0] - agent.goal[i][0]) + abs(pos[1] - agent.goal[i][1])
        if distance > self.t - save["time"][pos]:
            return float("inf")
        distance = pow(distance, 2)

        return distance
