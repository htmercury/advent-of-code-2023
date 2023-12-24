from pathlib import Path
from collections import defaultdict
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
hiking_lines = input_file.readlines()

# n, w, s, e
directions = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1)
]


def parse_inputs(lines):
    forest = set()
    slopes = {}
    start = None
    for y_idx, line in enumerate(lines):
        line = line.strip()
        for x_idx, spot in enumerate(line):
            if spot == '#':
                forest.add((y_idx, x_idx))
            elif spot != '.':
                slopes[(y_idx, x_idx)] = spot
            else:
                if not start:
                    start = (y_idx, x_idx)
                end = (y_idx, x_idx)

    return start, end, forest, slopes, len(lines), len(lines[0].strip())


def is_valid(pos, y_max, x_max):
    y_pos, x_pos = pos
    return y_pos >= 0 and y_pos < y_max and x_pos >= 0 and x_pos < x_max


def get_next_positions(curr_pos, forest, y_max, x_max):
    y, x = curr_pos
    for dy, dx in directions:
        new_pos = (y + dy, x + dx)
        if new_pos in forest:
            continue
        if is_valid(new_pos, y_max, x_max):
            yield new_pos


def get_adj_list(start, end, forest, y_max, x_max):
    junctions = defaultdict(set)

    stack = [(start, start, set([start]))]
    while len(stack) != 0:
        curr_pos, prev_pos, traversed = stack.pop()

        if curr_pos == end:
            end_junction = prev_pos
            end_length = len(traversed) - 1
            continue

        # avoid cyclic routes, check for looping
        if (curr_pos, len(traversed) - 1) in junctions[prev_pos]:
            continue

        next_positions = []
        for next_pos in get_next_positions(curr_pos, forest, y_max, x_max):
            if next_pos not in traversed:
                next_positions.append(next_pos)

        if len(next_positions) == 1:  # currently on a singular path, go next
            stack.append(
                (next_positions[0], prev_pos, traversed | set([next_positions[0]])))

        elif len(next_positions) > 1:  # reached a new junction
            steps = len(traversed) - 1
            junctions[prev_pos].add((curr_pos, steps))
            junctions[curr_pos].add((prev_pos, steps))

            # start new paths starting from a junction over again
            for new_pos in next_positions:
                stack.append((new_pos, curr_pos, set([curr_pos, new_pos])))

    return junctions, end_junction, end_length


def solution():
    start, end, forest, _, y_max, x_max = parse_inputs(hiking_lines)
    adj_list, end_junction, end_length = get_adj_list(
        start, end, forest, y_max, x_max)

    root_node = (start, set([start]), 0)
    stack = []
    stack.append(root_node)
    result = 0

    while len(stack) != 0:
        curr_pos, traversed, dist = stack.pop()

        # reduces search space knowing for last junction, need to choose one fixed path
        if curr_pos == end_junction:
            result = max(result, dist)
            continue

        for new_pos, length in adj_list[curr_pos]:
            if new_pos not in traversed:
                stack.append(
                    (new_pos, traversed | set([new_pos]), dist + length))

    return result + end_length


print(solution())
