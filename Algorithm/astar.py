from Global.DataStructure import *
from Search import *
from Global.variable import *
from Level.Level_1 import *
from Level.Level_2 import *
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
            agent.time = dict()
            agent.fuel = dict()
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
                        agent.generate_goal()

                if agent.current == agent.start:
                    (agent.trace[agent.start], agent.cost[agent.start], agent.eval[agent.start],
                     agent.time[agent.start], agent.fuel[agent.start]) = None, 0, 0, self.level.t, self.level.f
                agent.expanded.append(agent.current)
            for agent in agents.values():
                for move in MoveDirection.values():
                    next_pos = (agent.current[0] + move[0], agent.current[1] + move[1])
                    if self.cannot_move(next_pos):
                        continue
                    if (agent.time[agent.current] - 1 - level.map[next_pos[0]][next_pos[1]].value
                            - level.map[next_pos[0]][next_pos[1]].fuel < 0):
                        continue
                    if agent.fuel[agent.current] - 1 < 0:
                        continue
                    eval_score = agent.cost[agent.current] + 1 + self.level.heuristic(next_pos, agent, self.level)

                    if next_pos not in agent.expanded:
                        agent.eval[next_pos] = eval_score
                        agent.frontier.put((eval_score, next_pos))
                        agent.trace[next_pos] = agent.current
                        agent.cost[next_pos] = agent.cost[agent.current] + 1
                        agent.time[next_pos] = ((agent.time[agent.current] - 1
                                                - self.level.map[agent.current[0]][agent.current[1]].value)
                                                - self.level.map[agent.current[0]][agent.current[1]].fuel)
                        if self.level.map[next_pos[0]][next_pos[1]].fuel > 0:
                            agent.fuel[next_pos] = self.level.f
                        else:
                            agent.fuel[next_pos] = agent.fuel[agent.current] - 1
                print(agent.frontier.queue)
        self.trace = agents[0].trace
        print(self.trace[(5,5)])
        print(agents[0].fuel[(6,2)])
        return self.creat_path(agents[0])


if __name__ == '__main__':
    level = Level_2("./input1_level3.txt")
    algo = Astar(level)
    print(algo.run())
