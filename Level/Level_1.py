from Level.Level import Level


class Level_1(Level):
    def __init__(self, file_path):
        super().__init__(file_path)

    def write_algorithms_paths(self, bfs_path, dfs_path, gbfs_path,ucs_path, astar_path, file_name):
        output_file_name = file_name.replace("input", "output")
        with open(output_file_name, 'w') as file:
            file.write("BFS\n")
            for pos in bfs_path:
                file.write(f"{pos}\n")
            file.write("\nDFS\n")
            for pos in dfs_path:
                file.write(f"{pos}\n")
            file.write("\nGBFS\n")
            for pos in gbfs_path:
                file.write(f"{pos}\n")
            file.write("\nUCS\n")
            for pos in ucs_path:
                file.write(f"{pos}\n")
            file.write("\nAStar\n")
            for pos in astar_path:
                file.write(f"{pos}\n")

    def heuristic(self, pos, agent, save, goal_id, state):
        distance = abs(pos[0] - agent.goal[goal_id][0]) + abs(pos[1] - agent.goal[goal_id][1])
        for i in range(goal_id + 1, len(agent.goal)):
            distance += abs(pos[0] - agent.goal[i][0]) + abs(pos[1] - agent.goal[i][1])
        distance = pow(distance, 2)

        return distance
