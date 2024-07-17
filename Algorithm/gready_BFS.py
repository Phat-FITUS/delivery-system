from Global.DataStructure import *
from Search import *
from Global.variable import *
from Level.Level_1 import *
from Level.Level_2 import *
from Level.Level_3 import *

class GBFS(Search):
    def __init__(self, level):
        super().__init__(level)

    def run(self):
        agent = next(iter(self.level.agents.values()))  # pick the first agent
        agent.frontier = Frontier()
        agent.frontier.put((0, agent.start))  # push the start node to frontier
        agent.expanded = []
        agent.trace = {agent.start: None}  # trace the path

        while not agent.frontier.empty():
            _, current = agent.frontier.get()  # Get the node with the lowest cost

            if current == agent.goal:  # Check if the current node is the goal
                break

            agent.expanded.append(current)

            for move in MoveDirection.values():  # Loop through all possible moves
                next_pos = (current[0] + move[0], current[1] + move[1])

                if self.cannot_move(next_pos) or next_pos in agent.expanded:
                    continue

                if next_pos not in agent.trace:  # Check if the next node is not in the trace
                    agent.trace[next_pos] = current  # Add the next node to the trace
                    heuristic_cost = self.level.heuristic(next_pos, agent.goal)  # Calculate the heuristic cost
                    agent.frontier.put((heuristic_cost, next_pos))  # add the next node to the frontier

        return self.creat_path(agent)  
if __name__ == '__main__':
    level = Level_3("./input1_level3.txt")  
    algo = GBFS(level)
    print(algo.run())
   
