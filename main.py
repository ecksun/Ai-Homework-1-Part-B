import itertools
import copy
import sys
from heap import Heap

generated_nodes = 0

class Node(object):
    def __init__(self, position, parent, room_size, room, level):
        self.position = position
        self.parent = parent
        self.room = room
        self.level = level
        self.room_size = room_size

    def __str__(self):
        if self.parent:
            return '%s -> %s' % (self.parent.position, self.position)
        return 'root -> %s' % str((self.position))

    def print_room(self):
        print '-' * self.room_size[1] * 5 + '-'
        for i in reversed(xrange(0, self.room_size[0])):
            for j in xrange(0, self.room_size[1]):
                print '| ' + str(self.room[(i, j)]).rjust(2),
            print '|'
        print '-' * self.room_size[1] * 5 + '-'

    def possible_moves(self):
        x = self.position[0]
        y = self.position[1]
        moves = [(-4, -1, [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-4, -1)]),
                 (-1, -4, [(0, -1), (0, -2), (0, -3), (0, -4), (-1, -4)]),
                 (4, -1, [(1, 0), (2, 0), (3, 0), (4, 0), (4, -1)]),
                 (1, -4, [(0, -1), (0, -2), (0, -3), (0, -4), (1, -4)]),
                 (4, 1, [(1, 0), (2, 0), (3, 0), (4, 0), (4, 1)]),
                 (1, 4, [(0, 1), (0, 2), (0, 3), (0, 4), (1, 4)]),
                 (-4, 1, [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-4, 1)]),
                 (-1, 4, [(0, 1), (0, 2), (0, 3), (0, 4),  (-1, 4)])
                ]

        for mx, my, move_list in moves:
            if mx+x >= 0 and mx+x < self.room_size[0] and my+y >= 0 and my+y < self.room_size[1]:
                yield mx, my, [(i+x, j+y) for i, j in move_list]

    def is_finished(self, d):
        return sum(x == 0 for x in self.room.values()) <= d

    def copy(self, position):
        return Node(position, self, self.room_size, copy.copy(self.room), self.level+1)

def init_queue(size_x, size_y):
    r = {}
    for x in itertools.product(xrange(size_x), xrange(size_y)):
        r[x] = 0
    r[(0, 0)] = 1
    queue = []
    queue.append(Node((0, 0), None, (size_x, size_y), r, 1))
    return queue

def bfs(d, size_x, size_y):
    global generated_nodes
    queue = init_queue(size_x, size_y)
    while len(queue) != 0:
        node = queue.pop(0)
        for mx, my, moves in node.possible_moves():
            if not any([node.room[m] for m in moves]):
                new_node = node.copy(moves[-1])
                for m in moves:
                    new_node.room[m] = new_node.level

                if new_node.is_finished(d):
                    return new_node

                generated_nodes += 1
                queue.append(new_node)
    return False

def dfs(d, size_x, size_y):
    global generated_nodes
    queue = init_queue(size_x, size_y)
    while len(queue) != 0:
        node = queue.pop()
        for mx, my, moves in node.possible_moves():
            if not any([node.room[m] for m in moves]):
                new_node = node.copy(moves[-1])
                for m in moves:
                    new_node.room[m] = new_node.level

                if new_node.is_finished(d):
                    return new_node

                generated_nodes += 1
                queue.append(new_node)
    return False

def bestfs(d, size_x, size_y):
    return bestfs_overloaded(init_queue(size_x, size_y).pop(), d, size_x, size_y)

def bestfs_overloaded(node, d, size_x, size_y):
    global generated_nodes
    heap = Heap()
    for mx, my, moves in node.possible_moves():
        if not any([node.room[m] for m in moves]):
            new_node = node.copy(moves[-1])
            prio = priority(new_node, moves)
            for m in moves:
                new_node.room[m] = new_node.level

            if new_node.is_finished(d):
                return new_node

            generated_nodes += 1
            heap.add_task(prio, new_node)
    while True:
        next_node = heap.get_top_priority()
        if next_node != None:
            returnNode = bestfs_overloaded(next_node, d, size_x, size_y)
            if returnNode != False:
                return returnNode
        else:
            break
    return False

def priority(node, moves):
    prio = 0
    for m in moves:
        for i in [-1, 1]:
            for j in [-1, 1]:
                m = (m[0]+i, m[1]+j)
                try:
                    if node.room[m] != 0:
                        prio += 1
                except KeyError:
                    prio += 1
    return prio


if __name__ == '__main__':
    solutions = {'bfs': bfs, 'dfs': dfs, 'bestfs': bestfs}

    if len(sys.argv) == 5:
        size_x = int(sys.argv[1])
        size_y = int(sys.argv[2])
        d = int(sys.argv[3])
        solution = sys.argv[4]
        if solution in solutions:
            do = solutions[solution]
            room = do(d, size_x, size_y)
            if not room:
                print 'No solution found'
            else:
                room.print_room()
            print 'We generated %s nodes' % generated_nodes
        else:
            print 'python main.py size_x size_y d bfs|dfs|bestfs'
    else:
        room = bestfs(5, 11, 11)
        if not room:
            print 'No solution found'
        else:
            room.print_room()
        print 'We generated %s nodes' % generated_nodes
        print 'python main.py size_x size_y d bfs|dfs|bestfs'
