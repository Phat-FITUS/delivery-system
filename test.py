from Algorithm.BFS.BFS import BFS
from Algorithm.DFS.DFS import DFS
from Level.Level_1 import Level_1
from Level.Level_3 import Level_3
from Level.Level_4 import Level_4
from Algorithm.Min_N.min_n import MinN
from Algorithm.Astar.astar import Astar
import time

level = Level_1("./input1_level1.txt")
algo = DFS(level)

solve = algo.run()
print()