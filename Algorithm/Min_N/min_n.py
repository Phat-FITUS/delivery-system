import math

from Global.DataStructure import *
from ..Search import *
from Global.variable import *
from Level.Level_1 import *
from Level.Level_2 import *
from Level.Level_3 import *
from Level.Level_4 import *
import numpy as np
import time

class MinN(Search):
    def __init__(self, level):
        super().__init__(level)

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
                i = id + 1
                while True:
                    if i >= len(agents):
                        break
                    if agents[i].current == pos:
                        passing = True
                        break
                    i += 1
                if passing:
                    continue
                new_state = [pos, *state]
                all_states.append(new_state)
        return all_states
    def min_n(self, state, time, path, fuel, agents, goals, turn, costs, waits) -> (list, tuple):
        min_distances = abs(state[turn][0] - agents[turn].goal[goals[turn]][0]) + abs(state[turn][1] - agents[turn].goal[goals[turn]][1])
        if time > self.level.t or fuel > self.level.f:
            costs[turn] = float('inf')
            return [], (costs, state)
        if self.level.t - time < min_distances:
            costs[turn] = float('inf')
            return [], (costs, state)
        if self.level.f - fuel < min_distances:
            nearest = float("inf")
            for station in self.level.fuels:
                distance = (abs(state[turn][0] - station[0]) + abs(state[turn][1] - station[1]) + self.level.fuels[station] +
                            abs(agents[turn].goal[goals[turn]][0] - station[0]) + abs(agents[turn].goal[goals[turn]][1] - station[1]))
                if (abs(state[turn][0] - station[0]) + abs(state[turn][1] - station[1])) > self.level.f - fuel or self.level.t - time < distance:
                    continue
                if distance < nearest:
                    nearest = distance
            if math.isinf(nearest) and nearest > 0:
                costs[turn] = float('inf')
                return [], (costs, state)
        cost = pow(time, 2) + path
        for agent in agents.values():
            if state[agent.id] == agent.goal[goals[agent.id]]:
                costs[turn] = cost
                return [(state, goals, time)], (costs, state)
        print(state, time, turn)
        if self.level.map[state[turn][0]][state[turn][1]].fuel == 0:
            fuel = 0
        if turn == len(agents) - 1:
            next_turn = 0
        else:
            next_turn = turn + 1
        old_goals = goals
        all_cost = []
        all_child = []
        all_results = []
        all_move = []
        for move in MoveDirection.values():
            if waits[turn] > 0:
                next_pos = state[turn]
                all_move.append(next_pos)
                break
            next_pos = (state[turn][0] + move[0], state[turn][1] + move[1])
            conflict = False
            for i, pos in enumerate(state):
                if i != turn and pos == next_pos:
                    conflict = True
                    break
            if conflict:
                continue
            if self.cannot_move(next_pos):
                continue
            all_move.append(next_pos)
        for next_pos in all_move:
            next_state = state
            next_state = list(next_state)

            next_state[turn] = next_pos
            t = time
            p = path
            f = fuel
            if turn == len(agents) - 1:
                t += 1
            if next_pos != state[turn]:
                p += 1
                f += 1
            if waits[turn] > 0:
                waits[turn] -= 1
            else:
                waits[turn] = (self.level.map[next_pos[0]][next_pos[1]].value + self.level.map[next_pos[0]][next_pos[1]].fuel)
            result, (new_costs, new_state) = self.min_n(tuple(next_state), t, p, f, agents, goals, next_turn, costs, waits)
            all_cost.append(new_costs[turn])
            all_child.append((new_costs, new_state))
            all_results.append(result)
        min_cost = np.argmin(all_cost)
        min_result = all_results[min_cost]
        min_result.append((state, old_goals, time))
        return min_result, (all_child[min_cost][0], state)

    def run(self):
        start_time = time.time()
        agents = self.level.agents
        state = []
        for agent in agents.values():
            state.append(agent.start)
        results, (new_costs, new_state) = self.min_n(tuple(state), 0, 0, 0, agents, [0,0,0], 0, [float('inf'),float('inf'),float('inf')], [0,0,0])
        print(results)
        end_time = time.time()
        elapsed_time = float(end_time - start_time)
        print("elapsed_time:{0}".format(elapsed_time / 60) + "[min]")
        return results
