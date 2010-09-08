import pprint
import copy

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
            return str(self.parent.position) + ' -> ' + str(self.position) + "\n"
        else:
            return "root -> " + str(self.position) + "\n"

    def print_room(self):
        print ' --------------------------------------------------------'
        for i in range(0, self.room_size[0]):
            for j in range(0, self.room_size[1]):
                print '| ' + str(self.room[(i, j)]).rjust(2),
            print ' |'
        print ' --------------------------------------------------------'

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
        return Node(position, self, self.room_size, copy.deepcopy(self.room), self.level+1)

def bfs(d, size_x, size_y):
    global generated_nodes
    r = {}
    for i in xrange(size_x):
        for j in xrange(size_y):
            r[(i, j)] = 0
    r[(0, 0)] = 1
    queue = []
    queue.append(Node((0, 0), None, (size_x, size_y), r, 1))

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

room = bfs(5, 11, 11)
print "We are now done: "
room.print_room(11, 11)
print "We generated " + str(generated_nodes) + " nodes"
