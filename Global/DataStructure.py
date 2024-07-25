import heapq


class PriorityQueue:
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
            self.queue.append(item)
            self.queue.sort()
            return True
        else:
            return False

    def empty(self):
        return len(self.queue) == 0

    def get(self):
        # return heapq.heappop(self.queue)[1]
        return self.queue.pop(0)[1]
    def clear(self):
        self.queue = []

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        if item not in self.queue :
            self.queue.append(item)

    def dequeue(self):
        if len(self.queue):
            self.queue.pop(0)

    def empty(self):
        return len(self.queue) == 0

    def get(self):
        return self.queue[0]


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        if item not in self.stack:
            self.stack.append(item)

    def pop(self):
        if len(self.stack):
            self.stack.pop()

    def empty(self):
        return len(self.stack) == 0

    def get(self):
        return self.stack[-1]