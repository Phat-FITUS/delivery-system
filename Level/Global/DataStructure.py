import heapq


class Frontier:
    def __init__(self):
        self.queue = []

    def put(self, item):
        insert = True
        for element in self.queue:
            if element[1] == item[1]:
                if element[0] > item[0]:
                    self.queue.remove(element)
                else:
                    insert = False
        if insert:
            heapq.heappush(self.queue, item)

    def empty(self):
        return len(self.queue) == 0

    def get(self):
        return heapq.heappop(self.queue)[1]
