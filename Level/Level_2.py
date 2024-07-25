from Level.Level import Level
import math

class Level_2(Level):
    def __init__(self, file_path):
        super().__init__(file_path)

    def heuristic(self, pos, agent, save, goal_id, state):
        if self.t - save["time"][pos] < abs(pos[0] - agent.goal[goal_id][0]) + abs(pos[1] - agent.goal[goal_id][1]):
            return float("inf")
        distance = abs(pos[0] - agent.goal[goal_id][0]) + abs(pos[1] - agent.goal[goal_id][1])
        if state > 0:
            distance += state
        for i in range(goal_id + 1, len(agent.goal)):
            distance += abs(pos[0] - agent.goal[i][0]) + abs(pos[1] - agent.goal[i][1])
        distance = pow(distance, 2)

        return distance
