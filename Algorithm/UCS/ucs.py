from Global.DataStructure import *
from ..Search import *
from Global.variable import *
from Level.Level_1 import *
from Level.Level_2 import *
from Level.Level_3 import *
from Level.Level_4 import *

class UCS(Search):
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
        frontier = PriorityQueue()
        self.expanded = []
        state = []
        self.trace = dict()
        self.eval = dict()
        self.history = dict()
        finished = False
        for agent in agents.values():
            state.append(agent.start)
        frontier.put((0, (tuple(state), 0)))
        self.trace[(tuple(state), 0)] = None
        self.history[(tuple(state), 0)] = dict()
        (self.history[(tuple(state), 0)]["cost"], self.history[(tuple(state), 0)]["eval"], self.history[(tuple(state), 0)]["path"],
         self.history[(tuple(state), 0)]["time"], self.history[(tuple(state), 0)]["fuel"], self.history[(tuple(state), 0)]["goal"],
         self.history[(tuple(state), 0)]["state"], self.history[(tuple(state), 0)]["heuristic"]) = dict(),dict(), dict(), dict(), dict(), dict(), dict(), dict()
        i = 0
        initial_state = (tuple(state), 0)
        for pos in state:
            (self.history[(tuple(state), 0)]["cost"][pos], self.history[(tuple(state), 0)]["eval"][pos], self.history[(tuple(state), 0)]["path"][pos],
             self.history[(tuple(state), 0)]["time"][pos], self.history[(tuple(state), 0)]["fuel"][pos], self.history[(tuple(state), 0)]["state"][i], self.history[(tuple(state), 0)]["goal"][i], self.history[(tuple(state), 0)]["heuristic"][pos]) = 0,0,0, 0, 0, 0, 0, 0
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
                if agent.current == agent.goal[self.history[current_state]["goal"][i]]:
                    if agent.id == 0:
                        done = True
                        finished = True
                        self.expanded.append(current_state)
                        break
                    else:
                        if self.history[current_state]["goal"][i] == len(agent.goal) - 1:
                            agent.generate_goal(agents, self.level)
                        self.history[current_state]["goal"][i] += 1

                        new_goal.append(i)
                if math.isinf(self.history[current_state]["eval"][agent.current]) and self.history[current_state]["eval"][agent.current] > 0:
                    if agent.id == 0:
                        done = True
                        break
                    else:
                        current_state = initial_state
                        current, step = current_state
                        for id in agents:
                            agents[id].current = current[agents[id].id]
                        self.history[current_state]["state"][agent.id] = -1
                i += 1
            # return None
            if done is True:
                print(self.history[current_state])
                break
            if current_state not in self.expanded:
                self.expanded.append(current_state)
            if len(new_goal) > 0:
                i = 0
                for pos in current:
                    if i in new_goal:
                        self.history[current_state]["time"][pos] = 0
                        self.history[current_state]["path"][pos] = 0
                        heuristic = self.level.heuristic(agents[i].current, agents[i], self.history[current_state], self.history[current_state]["goal"][i], self.history[current_state]["state"][i])
                        if math.isinf(heuristic) and heuristic > 0:
                            self.history[current_state]["state"][i] = -1
                    i += 1
                initial_state = current_state
            all_pos = [[] for i in range(len(agents))]
            for agent in agents.values():
                if self.history[current_state]["state"][agent.id] != 0:
                    all_pos[agent.id] = [agent.current]
                    continue

                for move in MoveDirection.values():
                    next_pos = (agent.current[0] + move[0], agent.current[1] + move[1])
                    if self.cannot_move(next_pos):
                        continue
                    all_pos[agent.id].append(next_pos)
            for pos in all_pos:
                if len(pos) == 0:
                    for node in self.expanded:
                        print(node)
                    return 1
            states = self.create_state(0, agents, all_pos)
            save = dict()
            for state in states:
                state = tuple(state)
                if (state, step+1) not in self.expanded:
                    save = dict()
                    (save["cost"], save["eval"], save["path"],
                     save["time"],
                     save["fuel"], save["state"], save["heuristic"]) = dict(), dict(), dict(), dict(), dict(), dict(),dict()
                    total_eval = 0
                    i = 0
                    for next_pos in state:
                        if self.history[current_state]["state"][i] == -1:
                            save["path"][next_pos] = self.history[current_state]["path"][agents[i].current]
                            save["time"][next_pos] = self.history[current_state]["time"][agents[i].current]
                            save["state"][i] = -1
                            save["fuel"][next_pos] = self.history[current_state]["fuel"][agents[i].current]
                            save["eval"][next_pos] = self.history[current_state]["eval"][agents[i].current]
                            save["cost"][next_pos] = self.history[current_state]["cost"][agents[i].current]
                            save["heuristic"][next_pos] = self.history[current_state]["heuristic"][agents[i].current]
                            total_eval += save["eval"][next_pos]
                            continue
                        # print(next_pos)
                        # print(save["time"][next_pos])
                        if next_pos == agents[i].current:
                            save["path"][next_pos] = self.history[current_state]["path"][agents[i].current]
                        else:
                            save["path"][next_pos] = self.history[current_state]["path"][agents[i].current] + 1
                        save["time"][next_pos] = self.history[current_state]["time"][agents[i].current] + 1
                        if next_pos == agents[i].current and self.history[current_state]["state"][i] > 0:
                            save["state"][i] = self.history[current_state]["state"][i] - 1
                        else:
                            save["state"][i] = (self.level.map[next_pos[0]][next_pos[1]].value +
                                            self.level.map[next_pos[0]][next_pos[1]].fuel)
                        if self.level.map[next_pos[0]][next_pos[1]].fuel > 0:
                            save["fuel"][next_pos] = 0
                        else:
                            if next_pos == agents[i].current:
                                save["fuel"][next_pos] = self.history[current_state]["fuel"][agents[i].current]
                            else:
                                save["fuel"][next_pos] = self.history[current_state]["fuel"][agents[i].current] + 1
                        save["cost"][next_pos] = pow(save["time"][next_pos],2) + save["path"][next_pos]
                        save["heuristic"][next_pos] = self.level.heuristic(next_pos, agents[i], save, self.history[current_state]["goal"][i], save["state"][i])
                        eval_score = save["cost"][next_pos]
                        save["eval"][next_pos] = eval_score
                        total_eval += eval_score
                        i += 1
                    for pos in state:
                        if math.isinf(save["eval"][pos]):
                            total_eval = float('inf')
                            break

                    change = frontier.put((total_eval, (state, step + 1)))

                    if change:
                        self.eval[(state, step + 1)] = total_eval
                        self.trace[(state, step+1)] = current_state
                        self.history[(state, step+1)] = dict()
                        self.history[(state, step + 1)]["goal"] = dict()
                        (self.history[(state, step+1)]["cost"], self.history[(state, step+1)]["eval"], self.history[(state, step+1)]["path"],
                         self.history[(state, step+1)]["time"],
                         self.history[(state, step+1)]["fuel"], self.history[(state, step+1)]["state"],self.history[(state, step+1)]["heuristic"]) = dict(),dict(), dict(), dict(), dict(), dict(), dict()
                        i = 0
                        for pos in state:
                            self.history[(state, step+1)]["goal"][i] = self.history[current_state]["goal"][i]
                            self.history[(state, step+1)]["state"][i] = save["state"][i]
                            self.history[(state, step+1)]["heuristic"][pos] = save["heuristic"][pos]
                            self.history[(state, step + 1)]["cost"][pos] = save["cost"][pos]
                            (self.history[(state, step+1)]["eval"][pos], self.history[(state, step+1)]["path"][pos],
                             self.history[(state, step+1)]["time"][pos],
                             self.history[(state, step+1)]["fuel"][pos]) = (save["eval"][pos],
                                                             save["path"][pos], save["time"][pos], save["fuel"][pos])
                            i += 1
        if finished:
            solve = self.creat_path_2(self.expanded, self.trace)
            return solve
        return None


if __name__ == '__main__':
    level = Level_1("../../input1_level1.txt")
    algo = UCS(level)
    solve = algo.run()
    print(solve)
    print()

