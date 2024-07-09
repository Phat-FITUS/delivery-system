from Global.variable import *

class Level:
    def __init__(self, file_path):
        self.load(file_path)

    def load(self, file_name):
        # Load to initial variables
        # Map is a matrix of Position
        self.map = []  
        self.n = 0
        self.m = 0
        # Start and Goal are a Position
        self.start = None
        self.goal = None

        self.other_start = None
        self.other_goal = None

        with open(file_name, 'r') as file:
            # Đọc dòng đầu tiên để lấy kích thước bản đồ, thời gian giao hàng và dung lượng bình nhiên liệu
            first_line = file.readline().strip().split()
            self.n = int(first_line[0]) # hàng
            self.m = int(first_line[1]) # cột
            t = int(first_line[2]) # thời gian
            f = int(first_line[3]) # nhiên liệu

            # Đọc các dòng tiếp theo để lấy thông tin bản đồ
            for i in range(self.n):
                line = file.readline().strip()
                row = []
                for j, char in enumerate(line):
                    if char == '0':
                        row.append(Position(i, j, value=0))
                    elif char == '-1':
                        row.append(Position(i, j, value=-1))
                    elif char == 'S':
                        pos = Position(i, j, value=0)
                        row.append(pos)
                        self.start = pos
                    elif char == 'G':
                        pos = Position(i, j, value=0)
                        row.append(pos)
                        self.goal = pos
                    else:
                        row.append(Position(i, j, value=int(char)))
                self.map.append(row)

    def heuristic(self, pos, goal, current=None):
        pass

if __name__ == '__main__':
    level = Level("../input1 level1.txt")
    print(len(level.map))
    print(len(level.map[0]))
    for i in range(level.n):
        for j in range(level.m):
            print(level.map[i][j].value, end=" ")