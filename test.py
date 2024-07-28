from Algorithm.BFS.BFS import BFS
from Algorithm.DFS.DFS import DFS
from Algorithm.GBFS.GBFS import GBFS
from Level.Level_1 import Level_1
from Level.Level_3 import Level_3
from Level.Level_4 import Level_4
from Algorithm.Astar.astar import Astar
import time

start_time = time.time()
level = Level_4("./input2_level4.txt")
# print(level.count_walls((7, 2), (9, 9)))
algo = Astar(level)

solve = algo.run()
print(solve)
end_time = time.time()
elapsed_time = float(end_time - start_time)
print("elapsed_time:{0}".format(elapsed_time / 60) + "[min]")
# for state in solve:
#     print(state, algo.history[state])
print()