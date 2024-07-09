from Global.DataStructure import Frontier
from Search import *
from Global.variable import *


class Astar(Search):
    def __init__(self, level):
        super().__init__(level)
        self.time = dict()
        self.fuel = dict()

    def run(self, agents):
        done = False
        for agent in agents:
            agent.frontier = Frontier()
            agent.frontier.put((0, agent.start))
            agent.expanded = []
            agent.trace = dict()
            agent.cost = dict()
            agent.eval = dict()
            agent.time = dict()
            agent.fuel = dict()
        while True:
            if done is True:
                break
            for agent in agents:

                if agent.frontier.empty():
                    if agent.id != 0:
                        agent.generate_goal()
                    else:
                        done = True
                        break
                agent.current = agent.frontier.get()
                if self.level.map[agent.current[0]][agent.current[1]].agent is True:
                    pre = agent.current
                    agent.frontier.put((agent.eval[agent.current], agent.current))
                    agent.current = agent.frontier.get()
                    if agent.current == pre:
                        agent.frontier.put((agent.eval[agent.current], agent.current))
                        continue
                if agent.current == agent.goal:
                    if agent.id == 0:
                        done = True
                        break
                    else:
                        agent.generate_goal()

                if agent.current == agent.start:
                    agent.trace[self.level.start], agent.cost[self.level.start], agent.eval[self.level.start] = None, 0, 0
                agent.expanded.append(agent.current)
            for agent in agents:
                for move in MoveDirection.values():
                    next_pos = (agent.current[0] + move[0], agent.current[1] + move[1])
                    if self.cannot_move(next_pos):
                        continue
                    eval_score = agent.cost[agent.current] + 1 + self.level.heuristic(next_pos, self.level.goal, agent)

                    if next_pos not in self.expanded:
                        agent.eval[next_pos] = eval_score
                        agent.frontier.put((eval_score, next_pos))
                        agent.trace[next_pos] = agent.current
                        agent.cost[next_pos] = agent.cost[agent.current] + 1
                        agent.time[next_pos] = agent.time[agent.current] - 1 - self.level.map[agent.current[0]][agent.current[1]].value
                        agent.fuel[next_pos] = agent.fuel[agent.current] - 1 + self.level.map[agent.current[0]][agent.current[1]].fuel
        self.trace = agents[0].trace
        return agents



