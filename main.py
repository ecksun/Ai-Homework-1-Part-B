import pprint
import copy

visited_nodes = 0

def create_tree(x, y, size_x, size_y):
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
        if mx+x >= 0 and mx+x < size_x and my+y >= 0 and my+y < size_y:
            yield mx, my, [(i+x, j+y) for i,j in move_list]


class Node(object):

    def __init__(self, pos, parent, room, level):
        self.pos = pos
        self.parent = parent
        self.room = room
        self.level = level

    def __str__(self):
        if self.parent:
            return str(self.parent.pos) + ' -> ' + str(self.pos) + "\n"
        else:
            return "root -> " + str(self.pos) + "\n"

    def print_room(self, size_x, size_y):
        print ' --------------------------------------------------------'
        for i in range(0, size_x):
            for j in range(0, size_y):
                print '| ' + str(self.room[(i, j)]).rjust(2),
            print ' |'
        print ' --------------------------------------------------------'


def bfs(d, size_x, size_y):
    global visited_nodes
    r = {}
    for i in xrange(size_x):
        for j in xrange(size_y):
            r[(i, j)] = 0
    r[(0, 0)] = 1
    queue = []
    queue.append(Node((0, 0), None, r, 1))


    while len(queue) != 0:
        node = queue.pop(0)
        visited_nodes += 1
        # node.print_room(11, 11)
        for mx, my, moves in create_tree(node.pos[0], node.pos[1], size_x, size_y):
            if not any([node.room[m] for m in moves]):
                newroom = copy.deepcopy(node.room)
                for m in moves:
                    newroom[m] = node.level+1

                new_node = Node(moves[-1], node, newroom, node.level+1)
                if is_finished(newroom, d, size_x, size_y):
                    return new_node
                # if sum(newroom.values()) >= size_x * size_y - d:
                    # return node

                queue.append(new_node)

def is_finished(room, d, size_x, size_y):
    a = 0
    for i in range(size_x):
        for j in range(size_y):
            if room[(i, j)] == 0:
                a = a + 1
                if a > d:
                    return False
    return True
            

room = bfs(5, 11, 11)
print "We are now done: "
print room
room.print_room(11, 11)
print "We visited " + str(visited_nodes) + " nodes"
