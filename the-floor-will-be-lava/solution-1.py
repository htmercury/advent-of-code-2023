from pathlib import Path
from copy import copy, deepcopy
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
floor_lines = input_file.readlines()

# n,w,s,e
directions = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1)
]


def parse_inputs(lines):
    lines = list(map(lambda l: l.strip(), lines))
    y_max = len(lines)
    x_max = len(lines[0])
    return lines, y_max, x_max


def is_valid(pos, y_max, x_max):
    y_pos, x_pos = pos
    return y_pos >= 0 and y_pos < y_max and x_pos >= 0 and x_pos < x_max


def visualize_map(lines, energized):
    lines = copy(lines)
    lines = list(map(lambda l: list(l), lines))
    for y_pos, x_pos in energized:
        lines[y_pos][x_pos] = '#'
    for line in lines:
        print(''.join(line))

def move(pos, direction_idx):
    return (pos[0] + directions[direction_idx][0], pos[1] + directions[direction_idx][1])

def solution():
    parsed_lines, y_max, x_max = parse_inputs(floor_lines)
    # (pos, direction_idx)
    root_node = ((0, 0), 3)

    queue = []
    visited = set()
    energized = set()
    queue.append(root_node)
    visited.add(root_node)

    while len(queue) != 0:
        beam_pos, direction_idx = queue.pop(0)
        
        if is_valid(beam_pos, y_max, x_max):
            energized.add(beam_pos)
        else:
            continue

        new_nodes = []
        curr_tile = parsed_lines[beam_pos[0]][beam_pos[1]]
        if curr_tile == '.':
            new_nodes.append((move(beam_pos, direction_idx), direction_idx))
        elif curr_tile == '/':
            if direction_idx == 0:
                new_nodes.append((move(beam_pos, 3), 3))
            elif direction_idx == 3:
                new_nodes.append((move(beam_pos, 0), 0))
            elif direction_idx == 1:
                new_nodes.append((move(beam_pos, 2), 2))
            else:
                new_nodes.append((move(beam_pos, 1), 1))
        elif curr_tile == '\\':
            if direction_idx == 0:
                new_nodes.append((move(beam_pos, 1), 1))
            elif direction_idx == 1:
                new_nodes.append((move(beam_pos, 0), 0))
            elif direction_idx == 3:
                new_nodes.append((move(beam_pos, 2), 2))
            else:
                new_nodes.append((move(beam_pos, 3), 3))
        elif curr_tile == '|':
            if direction_idx == 0 or direction_idx == 2:
                new_nodes.append((move(beam_pos, direction_idx), direction_idx))
            else:
                new_nodes.append((beam_pos, 0))
                new_nodes.append((beam_pos, 2))
        else:  # '-'
            if direction_idx == 1 or direction_idx == 3:
                new_nodes.append((move(beam_pos, direction_idx), direction_idx))
            else:
                new_nodes.append((move(beam_pos, 1), 1))
                new_nodes.append((move(beam_pos, 3), 3))

        for new_node in new_nodes:
            if new_node not in visited:
                queue.append(new_node)
                visited.add(new_node)

    return len(energized)


print(solution())
