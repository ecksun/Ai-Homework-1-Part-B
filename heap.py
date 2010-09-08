import itertools
import heapq

class Heap(object):

    def __init__(self):
        self.pq = []                         # the priority queue list
        self.counter = itertools.count(1)    # unique sequence count
        self.task_finder = {}                # mapping of tasks to entries
        self.INVALID = 0                     # mark an entry as deleted

    def empty(self):
        self.pq = []
        self.counter = itertools.count(1)
        self.task_finder = {}

    def add_task(self, priority, task, count=None):
        if count is None:
            count = next(self.counter)
        entry = [priority, count, task]
        self.task_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def get_top_priority(self):
        while True:
            if (len(self.pq) > 0):
                priority, count, task = heapq.heappop(self.pq)
                del self.task_finder[task]
                if count is not self.INVALID:
                    return task
            else:
                return None

    def delete_task(self, task):
        entry = self.task_finder[task]
        entry[1] = self.INVALID

    def reprioritize(self, priority, task):
        entry = self.task_finder[task]
        add_task(priority, task, entry[1])
        entry[1] = self.INVALID

    def __str__(self):
        string = '\n' + str(len(self.pq)) + ':\n'
        for x in self.pq:
            string += "nodecontent:\t" + str(x) + "\n"
        return string

if __name__ == '__main__':
    heap = Heap()
    heap.add_task(10, 'a')
    heap.add_task(13, 'b')
    heap.add_task(53, 'c')
    heap.add_task(12, 'd')
    heap.add_task(5, 'e')
    print heap.get_top_priority()
