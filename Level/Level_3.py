from Level.Level import Level
import math


class Level_3(Level):
    def __init__(self, file_path):
        super().__init__(file_path)

    def heuristic(self, pos, agent, level):
        distance = abs(pos[0] - agent.goal[0]) + abs(pos[1] - agent.goal[1])
        nearest = distance

        if level.f- agent.fuel[agent.current] < distance:
            nearest = float('inf')
            for station in level.fuels:
                distance = (abs(pos[0] - station[0]) + abs(pos[1] - station[1]) + level.fuels[station] + abs(agent.goal[0] - station[0]) + abs(agent.goal[1] - station[1]))
                if (abs(pos[0] - station[0]) + abs(pos[1] - station[1])) > level.f - agent.fuel[agent.current] - 1:
                    continue
                if station in agent.expanded:
                    continue
                if distance < nearest:
                    nearest = distance

        return nearest
