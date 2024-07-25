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
            agent.heuristic = dict()
            # agent.trace[agent.goal] = None
        frontier.put((0, (tuple(state), 0)))
        trace[(tuple(state), 0)] = None
        history[(tuple(state), 0)] = dict()
        (history[(tuple(state), 0)]["cost"], history[(tuple(state), 0)]["eval"], history[(tuple(state), 0)]["path"],
         history[(tuple(state), 0)]["time"], history[(tuple(state), 0)]["fuel"], history[(tuple(state), 0)]["goal"],
         history[(tuple(state), 0)]["state"], history[(tuple(state), 0)]["heuristic"]) = dict(),dict(), dict(), dict(), dict(), dict(), dict(), dict()
        i = 0
        initial_state = (tuple(state), 0)
        for pos in state:
            (history[(tuple(state), 0)]["cost"][pos], history[(tuple(state), 0)]["eval"][pos], history[(tuple(state), 0)]["path"][pos],
             history[(tuple(state), 0)]["time"][pos], history[(tuple(state), 0)]["fuel"][pos], history[(tuple(state), 0)]["state"][i], history[(tuple(state), 0)]["goal"][i], history[(tuple(state), 0)]["heuristic"][pos]) = 0,0,0, 0, 0, 0, 0, 0
            i += 1
        while True:
            if done is True:
                break
            if frontier.empty():
                break
            current_state = frontier.get()
            current, step = current_state
            i = 0
            new_goal = []
            for agent in agents.values():
                agent.current = current[agent.id]
                if agent.current == agent.goal[history[current_state]["goal"][i]]:
                    if agent.id == 0:
                        done = True
                        print("ok1")
                        expanded.append(current_state)
                        break
                    else:
                        if history[current_state]["goal"][i] == len(agent.goal) - 1:
                            agent.generate_goal(agents, self.level)
                        history[current_state]["goal"][i] += 1

                        new_goal.append(i)
                if math.isinf(history[current_state]["eval"][agent.current]) and history[current_state]["eval"][agent.current] > 0:
                    if agent.id == 0:
                        done = True
                        break
                    else:
                        current_state = initial_state
                        current, step = current_state
                        for id in agents:
                            agents[id].current = current[agents[id].id]
                        history[current_state]["state"][agent.id] = -1
                i += 1
            # return None
            if done is True:
                print(history[current_state])
                break
            if current_state not in expanded:
                expanded.append(current_state)
            if len(new_goal) > 0:
                i = 0
                for pos in current:
                    if i in new_goal:
                        history[current_state]["time"][pos] = 0
                        history[current_state]["path"][pos] = 0
                        heuristic = self.level.heuristic(agents[i].current, agents[i], history[current_state], history[current_state]["goal"][i], history[current_state]["state"][i])
                        if math.isinf(heuristic) and heuristic > 0:
                            history[current_state]["state"][i] = -1
                    i += 1
                initial_state = current_state
            all_pos = [[] for i in range(len(agents))]
            for agent in agents.values():
                if history[current_state]["state"][agent.id] != 0:
                    all_pos[agent.id] = [agent.current]
                    continue

                for move in MoveDirection.values():
                    next_pos = (agent.current[0] + move[0], agent.current[1] + move[1])
                    print(next_pos)
                    if self.cannot_move(next_pos):
                        continue
                    if (history[current_state]["time"][agent.current] + 1 + level.map[next_pos[0]][next_pos[1]].value
                            + level.map[next_pos[0]][next_pos[1]].fuel > self.level.t):
                        agent.heuristic[next_pos] = float("inf")
                        all_pos[agent.id].append(next_pos)
                        continue

                    if history[current_state]["fuel"][agent.current] > self.level.f:
                        agent.heuristic[next_pos] = float("inf")
                        all_pos[agent.id].append(next_pos)
                        continue
                    agent.heuristic[next_pos] = None
                    all_pos[agent.id].append(next_pos)
            for pos in all_pos:
                if len(pos) == 0:
                    for node in expanded:
                        print(node)
                    return 1
            states = self.create_state(0, agents, all_pos)
            save = dict()
            for state in states:
                state = tuple(state)
                if (state, step+1) not in expanded:
                    save = dict()
                    (save["cost"], save["eval"], save["path"],
                     save["time"],
                     save["fuel"], save["state"], save["heuristic"]) = dict(), dict(), dict(), dict(), dict(), dict(),dict()
                    total_eval = 0
                    i = 0
                    for next_pos in state:
                        if history[current_state]["state"][i] == -1:
                            save["path"][next_pos] = history[current_state]["path"][agents[i].current]
                            save["time"][next_pos] = history[current_state]["time"][agents[i].current]
                            save["state"][i] = -1
                            save["fuel"][next_pos] = history[current_state]["fuel"][agents[i].current]
                            save["eval"][next_pos] = history[current_state]["eval"][agents[i].current]
                            save["cost"][next_pos] = history[current_state]["cost"][agents[i].current]
                            save["heuristic"][next_pos] = history[current_state]["heuristic"][agents[i].current]
                            total_eval += save["eval"][next_pos]
                            continue
                        # print(next_pos)
                        # print(save["time"][next_pos])
                        if next_pos == agents[i].current:
                            save["path"][next_pos] = history[current_state]["path"][agents[i].current]
                        else:
                            save["path"][next_pos] = history[current_state]["path"][agents[i].current] + 1
                        save["time"][next_pos] = history[current_state]["time"][agents[i].current] + 1
                        if next_pos == agents[i].current and history[current_state]["state"][i] > 0:
                            save["state"][i] = history[current_state]["state"][i] - 1
                        else:
                            save["state"][i] = (self.level.map[next_pos[0]][next_pos[1]].value +
                                            self.level.map[next_pos[0]][next_pos[1]].fuel)
                        if self.level.map[next_pos[0]][next_pos[1]].fuel > 0:
                            save["fuel"][next_pos] = 0
                        else:
                            if next_pos == agents[i].current:
                                save["fuel"][next_pos] = history[current_state]["fuel"][agents[i].current]
                            else:
                                save["fuel"][next_pos] = history[current_state]["fuel"][agents[i].current] + 1
                        save["cost"][next_pos] = pow(save["time"][next_pos],2) + save["path"][next_pos]
                        save["heuristic"][next_pos] = self.level.heuristic(next_pos, agents[i], history[current_state], history[current_state]["goal"][i], save["state"][i])
                        eval_score = save["cost"][next_pos] + save["heuristic"][next_pos]
                        save["eval"][next_pos] = eval_score
                        total_eval += eval_score
                        i += 1
                    for pos in state:
                        if math.isinf(save["eval"][pos]):
                            total_eval = float('inf')
                            break

                    change = frontier.put((total_eval, (state, step + 1)))

                    if change:
                        eval[(state, step + 1)] = total_eval
                        trace[(state, step+1)] = current_state
                        history[(state, step+1)] = dict()
                        history[(state, step + 1)]["goal"] = dict()
                        (history[(state, step+1)]["cost"], history[(state, step+1)]["eval"], history[(state, step+1)]["path"],
                         history[(state, step+1)]["time"],
                         history[(state, step+1)]["fuel"], history[(state, step+1)]["state"],history[(state, step+1)]["heuristic"]) = dict(),dict(), dict(), dict(), dict(), dict(), dict()
                        i = 0
                        for pos in state:
                            history[(state, step+1)]["goal"][i] = history[current_state]["goal"][i]
                            history[(state, step+1)]["state"][i] = save["state"][i]
                            history[(state, step+1)]["heuristic"][pos] = save["heuristic"][pos]
                            history[(state, step + 1)]["cost"][pos] = save["cost"][pos]
                            (history[(state, step+1)]["eval"][pos], history[(state, step+1)]["path"][pos],
                             history[(state, step+1)]["time"][pos],
                             history[(state, step+1)]["fuel"][pos]) = (save["eval"][pos],
                                                             save["path"][pos], save["time"][pos], save["fuel"][pos])
                            i += 1
        solve = self.creat_path_2(expanded, trace)
        print(solve)
        return solve


if __name__ == '__main__':
    level = Level_4("../input1_level3.txt")
    algo = Astar(level)
    solve = algo.run()
    print(solve)
    print()
    # agents = {0: 0,1: 1, 2:2}
    # all_pos = [[1,2,3],[1,2,3], [1,2,3] ]
    # print(create_state(id=0, agents=agents, all_pos=all_pos))
    # print(len(create_state(id=0, agents=agents, all_pos=all_pos)))

