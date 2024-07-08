from Global.DataStructure import Frontier
from .Search import *
from Global.variable import *

class UCS(Search):
    def __init__(self, level):
        super().__init__(level)
        self.time = dict()
        self.fuel = dict()

    def run(self):
        self.frontier = Frontier()
        self.frontier.put((0, self.level.start.pos))
        self.expanded = []
        self.trace = dict()
        cost = dict()
        self.time = dict()
        self.fuel = dict()
        # Duyệt tới khi nào không còn phần tử trong frontier
        while not self.frontier.empty():
            current = self.frontier.get()
           
            # Đã tới đích
            if current == self.level.goal.pos:
                break
            

            # Nếu là điểm bắt đầu -> khởi tạo giá trị
            if current == self.level.start.pos:
                self.trace[self.level.start], cost[self.level.start] = None, 0
            self.expanded.append(current)
            

            # Duyệt qua từng hướng đi
            for move in MoveDirection.values():
                next_pos = (current[0] + move[0], current[1] + move[1])
                if self.cannot_move(next_pos):
                    continue

                new_cost = cost[current] + 1  
                
                # Nếu điểm tiếp theo chưa được duyệt hoặc có giá trị mới nhỏ hơn giá trị cũ
                if next_pos not in self.expanded or new_cost < cost.get(next_pos, float('inf')):
                    cost[next_pos] = new_cost
                    self.frontier.put((new_cost, next_pos))
                    self.trace[next_pos] = current
                    self.time[next_pos] = self.time[current] + 1 + self.level.map[current[0]][current[1]].value
                    self.fuel[next_pos] = self.fuel[current] + 1 + self.level.map[current[0]][current[1]].fuel
        return self.creat_path()