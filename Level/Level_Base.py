from Global.variable import Agent
from Level.Level import Level


class Level_Base(Level):
    def __init__(self):
        pass
    def copy(self, map, m, n, t, f, agent, walls, fuels):
        self.map = map
        self.m = m
        self.n = n
        self.t = t
        self.f = f
        new_agent = Agent(start=agent.current)
        self.agents = dict()
        self.agents[0] = new_agent
        self.walls = walls
        self.fuels = fuels

    def heuristic(self, pos, agent, save, goal_id, state):
        distance = abs(pos[0] - agent.goal[goal_id][0]) + abs(pos[1] - agent.goal[goal_id][1])
        for i in range(goal_id + 1, len(agent.goal)):
            distance += abs(pos[0] - agent.goal[i][0]) + abs(pos[1] - agent.goal[i][1])
        distance = pow(distance, 2)

        return False, distance