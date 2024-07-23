from Level.Level import Level
import math


class Level_4(Level):
    def __init__(self, file_path):
        super().__init__(file_path)

    def heuristic(self, pos, agent, history):
        print(agent.goal)
        distance = abs(pos[0] - agent.goal[0]) + abs(pos[1] - agent.goal[1])
        if self.f - history["fuel"][agent.current] < distance:
            nearest = float("inf")

            for station in self.fuels:
                # print("bafdjhefbjhrejhghe")
                # print(pos)
                # print(station)
                # print(agent.goal[i])
                distance = (pow((abs(pos[0] - station[0]) + abs(pos[1] - station[1]) + self.fuels[station] +
                                 abs(agent.goal[0] - station[0]) + abs(agent.goal[1] - station[1])), 2) +
                            (abs(pos[0] - station[0]) + abs(pos[1] - station[1]) + self.fuels[station] +
                             abs(agent.goal[0] - station[0]) + abs(agent.goal[1] - station[1])))
                # print(history["fuel"][agent.current])
                if (abs(pos[0] - station[0]) + abs(pos[1] - station[1])) > self.f - history["fuel"][agent.current] - 1:
                    continue
                if distance < nearest:
                    nearest = distance
            distance = nearest
        print(distance)
        return distance
