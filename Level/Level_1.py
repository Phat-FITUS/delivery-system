from Level.Level import Level


class Level_1(Level):
    def __init__(self, file_path):
        super().__init__(file_path)

    def heuristic(self, pos, agent, save, goal_id, state):
        distance = abs(pos[0] - agent.goal[goal_id][0]) + abs(pos[1] - agent.goal[goal_id][1])
        for i in range(goal_id + 1, len(agent.goal)):
            distance += abs(pos[0] - agent.goal[i][0]) + abs(pos[1] - agent.goal[i][1])
        distance = pow(distance, 2)

        return distance
