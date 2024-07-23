from Global.DataStructure import *
from Search import *
from Global.variable import *
from Level.Level_1 import *
from Level.Level_2 import *
from Level.Level_3 import *
from Level.Level_4 import *

class Astar(Search):
    def __init__(self, level):
        super().__init__(level)
        self.time = dict()
        self.fuel = dict()
    def create_state(self, id, agents, all_pos):
        if id == len(agents) - 1:
            return [[pos] for pos in all_pos[id]]
        all_small_state = self.create_state(id + 1, agents, all_pos)
        all_states = []
        for pos in all_pos[id]:
            for state in all_small_state:
                if pos in state:
                    continue
                passing = False
                i = id+1
                while True:
                    if i >= len(agents):
                        break
                    if agents[i].current == pos:
                        passing = True
                        break
                    i+=1
                if passing:
                    continue
                new_state = [pos, *state]
                all_states.append(new_state)
        return all_states
    def run(self):
        agents = self.level.agents
        done = False
        frontier = Frontier()
        expanded = []
        states = []
        state = []
        trace = dict()
        eval = dict()
        history = dict()
        for agent in agents.values():
            state.append(agent.start)
            agent.expanded = []
            agent.trace = dict()

            agent.cost = dict()
            agent.eval = dict()
            agent.path = dict()
            agent.time = dict()
            agent.fuel = dict()
            agent.heuristic = dict()
            # agent.trace[agent.goal] = None
        frontier.put((0, tuple(state)))
        trace[tuple(state)] = None
        history[tuple(state)] = dict()
        (history[tuple(state)]["cost"], history[tuple(state)]["eval"], history[tuple(state)]["path"],
         history[tuple(state)]["time"], history[tuple(state)]["fuel"]) = dict(), dict(), dict(), dict(), dict()
        i = 0
        for pos in state:
            (history[tuple(state)]["cost"][pos], history[tuple(state)]["eval"][pos], history[tuple(state)]["path"][pos],
             history[tuple(state)]["time"][pos], history[tuple(state)]["fuel"][pos]) = 0, 0, 0, 0, 0
            i += 1
        while True:
            if done is True:
                break
            if frontier.empty():
                break
            current = frontier.get()
            print(len(agents))
            i = 0
            new_goal = []
            for agent in agents.values():
                agent.current = current[agent.id]
                print(agent.id)
                print("-----------------")
                print(current)
                if agent.current == agent.goal:
                    if agent.id == 0:
                        done = True
                        print("ok1")
                        break
                    else:
                        agent.generate_goal(agents, self.level)
                        new_goal.append(i)
                if math.isinf(history[current]["eval"][agent.current]) and history[current]["eval"][agent.current] > 0:
                    if agent.id == 0:
                        print("ok2")
                        done = True
                        break
                    else:
                        print("ok")
                        agent.generate_goal(self.level)
                        print("ok4")
                        # agent.generate_goal(self.level)
                        done = True
                        expanded.append(current)
                        break
                i += 1
            # return None
            if done is True:
                print(history[current])
                break
            expanded.append(current)
            if len(new_goal) > 0:
                i = 0
                for pos in current:
                    if i in new_goal:
                        history[current]["time"][pos] = 0
                        history[current]["path"][pos] = 0

                    i += 1
                frontier.clear()
            all_pos = [[] for i in range(len(agents))]
            for agent in agents.values():
                print(agent.current)
                print("________________________________")
                for move in MoveDirection.values():
                    next_pos = (agent.current[0] + move[0], agent.current[1] + move[1])
                    print(next_pos)
                    if self.cannot_move(next_pos):
                        continue
                    print(1)
                    print(current)
                    print(agent.current)
                    print(history[current])
                    agent.heuristic[next_pos] = self.level.heuristic(next_pos, agent, history[current])
                    if (history[current]["time"][agent.current] + 1 + level.map[next_pos[0]][next_pos[1]].value
                            + level.map[next_pos[0]][next_pos[1]].fuel > self.level.t):
                        agent.heuristic[next_pos] = float("inf")
                        all_pos[agent.id].append(next_pos)
                        continue
                    print(2)

                    if history[current]["fuel"][agent.current] > self.level.f:
                        agent.heuristic[next_pos] = float("inf")
                        all_pos[agent.id].append(next_pos)
                        continue
                    print(3)

                    print("======================")
                    all_pos[agent.id].append(next_pos)
            print(current)
            print(all_pos)
            for pos in all_pos:
                if len(pos) == 0:
                    for node in expanded:
                        print(node)
                    return 1
            states = self.create_state(0, agents, all_pos)
            # print(states)
            # print(history)
            save = dict()
            for state in states:
                state = tuple(state)
                if state not in expanded:
                    save = dict()
                    (save["cost"], save["eval"], save["path"],
                     save["time"],
                     save["fuel"]) = dict(), dict(), dict(), dict(), dict()
                    total_eval = 0
                    i = 0
                    for next_pos in state:
                        save["path"][next_pos] = history[current]["path"][agents[i].current] + 1
                        if next_pos == agents[i].current:
                            save["time"][next_pos] = history[current]["time"][agents[i].current] + 1
                        else:
                            save["time"][next_pos] = ((history[current]["time"][agents[i].current] + 1
                                                 + self.level.map[next_pos[0]][next_pos[1]].value)
                                                + self.level.map[next_pos[0]][next_pos[1]].fuel)
                        # print(next_pos)
                        # print(save["time"][next_pos])
                        if self.level.map[next_pos[0]][next_pos[1]].fuel > 0:
                            save["fuel"][next_pos] = 0
                        else:
                            if next_pos == agents[i].current:
                                save["fuel"][next_pos] = history[current]["fuel"][agents[i].current]
                            else:
                                save["fuel"][next_pos] = history[current]["fuel"][agents[i].current] + 1
                        eval_score = pow(save["time"][next_pos],2) + save["path"][next_pos] + agents[i].heuristic[next_pos]
                        save["eval"][next_pos] = eval_score
                        total_eval += eval_score
                        i += 1
                    for pos in state:
                        if math.isinf(save["eval"][pos]):
                            total_eval = float('inf')
                            break
                    change = frontier.put((total_eval, state))
                    eval[state] = total_eval
                    if change:
                        trace[state] = current
                        history[state] = dict()
                        (history[state]["cost"], history[state]["eval"], history[state]["path"],
                         history[state]["time"],
                         history[state]["fuel"]) = dict(), dict(), dict(), dict(), dict()
                        i = 0
                        for pos in state:
                            (history[state]["eval"][pos], history[state]["path"][pos],
                             history[state]["time"][pos],
                             history[state]["fuel"][pos]) = (save["eval"][pos],
                                                             save["path"][pos], save["time"][pos], save["fuel"][pos])
                            i += 1

            print()
            print(frontier.queue)
            print()
            # for agent in agents.values():
            #     print(agent.id)
            #     print(agent.eval)
        for node in expanded:
            print(node)
        solve = self.creat_path_2(expanded, trace)
        print(solve)
        return solve


if __name__ == '__main__':
    level = Level_4("../input1_level4.txt")
    algo = Astar(level)
    solve = algo.run()
    print(solve)
    print()
    # agents = {0: 0,1: 1, 2:2}
    # all_pos = [[1,2,3],[1,2,3], [1,2,3] ]
    # print(create_state(id=0, agents=agents, all_pos=all_pos))
    # print(len(create_state(id=0, agents=agents, all_pos=all_pos)))

