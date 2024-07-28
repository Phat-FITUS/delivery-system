import re

from Global.variable import *


class Level:
    def __init__(self, file_path):
        self.load(file_path)

    def write_path_to_file(self, path, file_name):
        output_file_name = file_name.replace("input", "output")
        with open(output_file_name, 'w') as file:
            for pos in path:
                file.write(f"{pos}\n")

    def load(self, file_name):
        # Load to initial variables
        # Map is a matrix of Position
        self.map = []  
        self.n = 0
        self.m = 0
        # Start and Goal are a Position
        self.agents = dict()
        self.fuels = dict()
        self.walls = dict()

        walls_list = []

        with open(file_name, 'r') as file:
            # Đọc dòng đầu tiên để lấy kích thước bản đồ, thời gian giao hàng và dung lượng bình nhiên liệu
            first_line = file.readline().strip().split()
            self.n = int(first_line[0]) # hàng
            self.m = int(first_line[1]) # cột
            self.t = int(first_line[2]) # thời gian
            self.f = int(first_line[3]) # nhiên liệu

            # Đọc các dòng tiếp theo để lấy thông tin bản đồ
            for i in range(self.n):
                line = file.readline().strip().split()
                row = []
                for j, char in enumerate(line):
                    # print(char, end="/")
                    if char == '-1':
                        walls_list.append((i, j))
                        row.append(Position(i, j, value=-1))

                    elif re.match(r"\d", char):
                        row.append(Position(i, j, value=int(char)))

                    elif char == 'S':
                        pos = Position(i, j, value=0)
                        row.append(pos)
                        if 0 in self.agents.keys():
                            self.agents[0].start = (i, j)
                        else:
                            self.agents[0] = Agent((i, j), id=0)
                    elif char == 'G':
                        pos = Position(i, j, value=0)
                        row.append(pos)
                        if 0 in self.agents.keys():
                            self.agents[0].goal.append((i, j))
                        else:
                            self.agents[0] = Agent(goal=(i, j), id=0)
                    elif re.match(r"S\d", char):
                        pos = Position(i, j, value=0)
                        row.append(pos)
                        if int(char[1]) in self.agents.keys():
                            self.agents[int(char[1])].start = (i, j)
                        else:
                            self.agents[int(char[1])] = Agent((i, j), id=int(char[1]))
                    elif re.match(r'G\d', char):
                        pos = Position(i, j, value=0)
                        row.append(pos)
                        if int(char[1]) in self.agents.keys():
                            self.agents[int(char[1])].goal.append((i, j))
                        else:
                            self.agents[int(char[1])] = Agent(goal=(i, j), id=int(char[1]))
                    elif re.match(r'F\d', char):
                        pos = Position(i, j, value=0, fuel=int(char[1]))
                        self.fuels[(i, j)] = int(char[1])
                        row.append(pos)
                    else:
                        continue
                self.map.append(row)
            self.walls["row"] = [[] for i in range(self.n)]
            self.walls["col"] = [[] for i in range(self.m)]
            for wall in walls_list:
                self.walls["row"][wall[0]].append(wall[1])
                self.walls["row"][wall[0]].sort()
                self.walls["col"][wall[1]].append(wall[0])
                self.walls["col"][wall[1]].sort()



if __name__ == '__main__':
    level = Level("../input1_level4.txt")
    print(level.agents[0].goal)
    for i in range(level.n ):
        for j in range(level.m ):
            print(level.map[i][j].value+level.map[i][j].fuel, end=" ")
        print('\n')