import itertools
import heapq

class Heap(object):

    def __init__(self):
        self.pq = []                         # the priority queue list
        self.counter = itertools.count(1)    # unique sequence count
        self.task_finder = {}                # mapping of tasks to entries
        self.INVALID = 0                     # mark an entry as deleted

    def add_task(self, priority, task, count=None):
        if count is None:
            count = next(self.counter)
        entry = [priority, count, task]
        self.task_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def get_top_priority(self):
        while True:
            priority, count, task = heapq.heappop(self.pq)
            del self.task_finder[task]
            if count is not self.INVALID:
                return task

    def delete_task(self, task):
        entry = self.task_finder[task]
        entry[1] = self.INVALID

    def reprioritize(self, priority, task):
        entry = self.task_finder[task]
        add_task(priority, task, entry[1])
        entry[1] = self.INVALID

if __name__ == '__main__':
    heap = Heap()
    heap.add_task(10, 'a')
    heap.add_task(13, 'b')
    heap.add_task(53, 'c')
    heap.add_task(12, 'd')
    heap.add_task(5, 'e')
    print heap.get_top_priority()
