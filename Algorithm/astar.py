from Global.DataStructure import *
from Search import *
from Global.variable import *
from Level.Level_1 import *
from Level.Level_2 import *
from Level.Level_3 import *
class Astar(Search):
    def __init__(self, level):
        super().__init__(level)
        self.time = dict()
        self.fuel = dict()

    def run(self):
        agents = self.level.agents
        done = False

        for agent in agents.values():
            agent.frontier = Frontier()
            agent.frontier.put((0, agent.start))
            agent.expanded = []
            agent.trace = dict()
            agent.cost = dict()
            agent.eval = dict()
            agent.path = dict()
            agent.time = dict()
            agent.fuel = dict()
            agent.trace[agent.goal] = None
        while True:
            if done is True:
                break
            for agent in agents.values():

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
                        agent.generate_goal(self.level)

                if agent.current == agent.start:
                    (agent.trace[agent.start], agent.cost[agent.start], agent.eval[agent.start],
                     agent.path[agent.start], agent.time[agent.start], agent.fuel[agent.start]) = None, 0, 0, 0, 0, 0
                elif math.isinf(agent.eval[agent.current]) and agent.eval[agent.current] > 0:
                    break
                agent.expanded.append(agent.current)

                for move in MoveDirection.values():
                    next_pos = (agent.current[0] + move[0], agent.current[1] + move[1])
                    if self.cannot_move(next_pos):
                        continue
                    if (agent.time[agent.current] + 1 + level.map[next_pos[0]][next_pos[1]].value
                            + level.map[next_pos[0]][next_pos[1]].fuel > self.level.t):

                        continue
                    if agent.fuel[agent.current] > self.level.f:
                        continue
                    if next_pos not in agent.expanded:
                        agent.path[next_pos] = agent.path[agent.current] + 1
                        agent.time[next_pos] = ((agent.time[agent.current] + 1
                                                 + self.level.map[agent.current[0]][agent.current[1]].value)
                                                + self.level.map[agent.current[0]][agent.current[1]].fuel)
                        eval_score = pow(agent.time[next_pos],2) + agent.path[next_pos] + self.level.heuristic(next_pos, agent, self.level)
                        agent.eval[next_pos] = eval_score
                        change = agent.frontier.put((eval_score, next_pos))
                        if change:
                            agent.trace[next_pos] = agent.current

                        if self.level.map[next_pos[0]][next_pos[1]].fuel > 0:
                            agent.fuel[next_pos] = 0
                        else:
                            agent.fuel[next_pos] = agent.fuel[agent.current] + 1
                print(agent.frontier.queue)
        return [self.creat_path(agents[i]) for i in agents]


if __name__ == '__main__':
    level = Level_3("./input1_level2.txt")
    algo = Astar(level)
    print(algo.run())
