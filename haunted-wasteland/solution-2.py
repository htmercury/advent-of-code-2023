from pathlib import Path
import math
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
map_lines = input_file.readlines()


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def parse_inputs(lines):
    node_value_map = {}
    pattern = list(lines[0].strip())
    lines = lines[2:]
    for line in lines:
        line = line.strip()
        src, dst = line.split(' = ')
        dst = dst[1:-1]
        left_dst, right_dst = dst.split(', ')
        if src not in node_value_map:
            node_value_map[src] = Node(src)
        src_node = node_value_map[src]
        if left_dst not in node_value_map:
            node_value_map[left_dst] = Node(left_dst)
        left_node = node_value_map[left_dst]
        if right_dst not in node_value_map:
            node_value_map[right_dst] = Node(right_dst)
        right_node = node_value_map[right_dst]
        src_node.left = left_node
        src_node.right = right_node
    
    return pattern, node_value_map

def get_steps(pattern, root_node):
    i = 0
    while root_node.value[-1] != 'Z':
        direction = pattern[i % len(pattern)]
        if direction == 'L':
            # print(root_node.left.value)
            root_node = root_node.left
        else:
            # print(root_node.right.value)
            root_node = root_node.right
        i += 1
    
    return i

def solution():
    pattern, node_value_map = parse_inputs(map_lines)
    root_nodes = list(filter(lambda n: n[-1] == 'A', node_value_map.keys()))
    steps_list = []
    for root_node in root_nodes:
        root_node = node_value_map[root_node]
        steps = get_steps(pattern, root_node)
        steps_list.append(steps)
    
    return math.lcm(*steps_list)


print(solution())
