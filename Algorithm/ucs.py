from Global.DataStructure import *
from Search import *
from Global.variable import *
from Level.Level_1 import *
from Level.Level_2 import *
from Level.Level_3 import *

class UCS(Search):
    def __init__(self, level):
        super().__init__(level)

    def run(self):
        agent = next(iter(self.level.agents.values()))  # pick the first agent
        agent.frontier = Frontier()
        agent.frontier.put((0, agent.start))  # push the start node with initial cost to frontier
        agent.expanded = []
        agent.trace = {agent.start: None}  # trace the path
        agent.cost = {agent.start: 0}  # cost from start node to this node

        while not agent.frontier.empty():
            current_cost, current = agent.frontier.get()  # Get the node with the lowest total cost

            if current == agent.goal:  # Check if the current node is the goal
                break

            agent.expanded.append(current)

            for move in MoveDirection.values():  # Loop through all possible moves
                next_pos = (current[0] + move[0], current[1] + move[1])
                new_cost = current_cost + self.level.cost(current, next_pos)  # Calculate new cost

                if self.cannot_move(next_pos) or next_pos in agent.expanded:
                    continue

                if next_pos not in agent.cost or new_cost < agent.cost[next_pos]:  # Check if new cost is cheaper
                    agent.trace[next_pos] = current  # Add the next node to the trace
                    agent.cost[next_pos] = new_cost  # Update the cost
                    agent.frontier.put((new_cost, next_pos))  # add the next node to the frontier with its new cost

        return self.create_path(agent)  # This should be create_path, not creat_path

if __name__ == '__main__':
    level = Level_3("./input1_level3.txt")  
    algo = UCS(level)
    print(algo.run())