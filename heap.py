import itertools
class Heap(object):
    def __init__(self):
        pq = []                         # the priority queue list
        counter = itertools.count(1)    # unique sequence count
        task_finder = {}                # mapping of tasks to entries
        INVALID = 0                     # mark an entry as deleted

    def add_task(self, priority, task, count=None):
        if count is None:
            count = next(self.counter)
        entry = [priority, count, task]
        self.task_finder[task] = entry
        heappush(self.pq, entry)

    def get_top_priority(self):
        while True:
            priority, count, task = heappop(self.pq)
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

