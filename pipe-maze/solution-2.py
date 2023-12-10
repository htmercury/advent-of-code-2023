from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
pipe_lines = input_file.readlines()


class Node:
    def __init__(self, pos):
        self.pos = pos
        self.pipe = None
        self.prev = None
        self.next = None


def get_prev_next_pos(pos, pipe):
    y_pos, x_pos = pos
    if pipe == '|':
        return [(y_pos + 1, x_pos), (y_pos - 1, x_pos)]
    elif pipe == '-':
        return [(y_pos, x_pos - 1), (y_pos, x_pos + 1)]
    elif pipe == 'L':
        return [(y_pos, x_pos + 1), (y_pos - 1, x_pos),]
    elif pipe == 'J':
        return [(y_pos, x_pos - 1), (y_pos - 1, x_pos)]
    elif pipe == '7':
        return [(y_pos, x_pos - 1), (y_pos + 1, x_pos)]
    else:
        return [(y_pos + 1, x_pos), (y_pos, x_pos + 1)]  # F


def parse_inputs(lines):
    pipes = ['|', '-', 'L', 'J', '7', 'F']
    node_value_map = {}
    for y_idx, line in enumerate(lines):
        line = line.strip()
        for x_idx, pipe_ground in enumerate(line):
            if pipe_ground in pipes:
                pos = (y_idx, x_idx)
                if pos not in node_value_map:
                    node_value_map[pos] = Node(pos)
                prev, next = get_prev_next_pos(pos, pipe_ground)
                if prev not in node_value_map:
                    node_value_map[prev] = Node(prev)
                if next not in node_value_map:
                    node_value_map[next] = Node(next)

                node_value_map[pos].pipe = pipe_ground
                node_value_map[pos].prev = node_value_map[prev]
                node_value_map[pos].next = node_value_map[next]
            if pipe_ground == 'S':
                root_pos = (y_idx, x_idx)

    prev, next = get_starting_prev_next(node_value_map, root_pos)
    root_node = node_value_map[root_pos]
    root_node.prev = prev
    root_node.next = next
    root_node.pipe = get_root_node_pipe(root_node)

    return node_value_map, root_node


def get_starting_prev_next(node_value_map, root_pos):
    y_pos, x_pos = root_pos
    positions = []
    if (y_pos + 1, x_pos) in node_value_map and node_value_map[(y_pos + 1, x_pos)].next.pos == root_pos:
        positions.append((y_pos + 1, x_pos))
    if (y_pos, x_pos - 1) in node_value_map and node_value_map[(y_pos, x_pos - 1)].next.pos == root_pos:
        positions.append((y_pos, x_pos - 1))

    if (y_pos - 1, x_pos) in node_value_map and node_value_map[(y_pos - 1, x_pos)].prev.pos == root_pos:
        positions.append((y_pos - 1, x_pos))
    if (y_pos, x_pos + 1) in node_value_map and node_value_map[(y_pos, x_pos + 1)].prev.pos == root_pos:
        positions.append((y_pos, x_pos + 1))

    prev, next = positions

    return node_value_map[prev], node_value_map[next]


def fix_loop(start):
    prev_node = start
    curr_node = start.next

    loop_pos_list = [start.pos]

    while curr_node != start:  # root node
        loop_pos_list.append(curr_node.pos)
        if curr_node.prev != prev_node:
            curr_node.next = curr_node.prev
            curr_node.prev = prev_node
        prev_node = curr_node
        curr_node = curr_node.next

    return loop_pos_list


def get_root_node_pipe(root_node):
    positions = [root_node.prev.pos, root_node.next.pos]
    y_pos, x_pos = root_node.pos

    if set([(y_pos + 1, x_pos), (y_pos - 1, x_pos)]) == set(positions):
        return '|'
    elif set([(y_pos, x_pos - 1), (y_pos, x_pos + 1)]) == set(positions):
        return '-'
    elif set([(y_pos, x_pos + 1), (y_pos - 1, x_pos)]) == set(positions):
        return 'L'
    elif set([(y_pos, x_pos - 1), (y_pos - 1, x_pos)]) == set(positions):
        return 'J'
    elif set([(y_pos, x_pos - 1), (y_pos + 1, x_pos)]) == set(positions):
        return '7'
    else:
        return 'F'


def solution():
    node_value_map, root_node = parse_inputs(pipe_lines)
    loop_pos_list = fix_loop(root_node)  # sets prev and next to loop properly

    y_max = len(pipe_lines)
    x_max = len(pipe_lines[0].strip())

    enclosed = 0
    for j in range(y_max):
        counter = 0
        pipe_parity_list = ['|', 'J', 'L']
        for i in range(x_max):
            if (j, i) in loop_pos_list and node_value_map[(j, i)].pipe in pipe_parity_list:
                counter += 1
            if (j, i) not in loop_pos_list and counter % 2 != 0:
                enclosed += 1

    return enclosed


print(solution())
