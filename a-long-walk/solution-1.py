from pathlib import Path
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

slope_directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}


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


def solution():
    start, end, forest, slopes, y_max, x_max = parse_inputs(hiking_lines)

    root_node = (start, set([start]))
    stack = []
    stack.append(root_node)

    result = 0

    while len(stack) != 0:
        curr_pos, traversed = stack.pop()
        y, x = curr_pos
        adj_dx = directions

        if curr_pos == end:
            result = max(result, len(traversed) - 1)
            continue

        if curr_pos in slopes:
            adj_dx = [slope_directions[slopes[curr_pos]]]
            new_pos = (y + dy, x + dx)

        for dy, dx in adj_dx:
            new_pos = (y + dy, x + dx)
            if new_pos in forest:
                continue
            if new_pos not in traversed and is_valid(new_pos, y_max, x_max):
                stack.append((new_pos, traversed | set([new_pos])))

    return result


print(solution())
