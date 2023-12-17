import heapq
from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
traffic_lines = input_file.readlines()

# n, w, s, e
directions = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1)
]

MAX_MOVES = 3


def parse_inputs(lines):
    lines = list(map(lambda l: list(l.strip()), lines))
    return lines, len(lines), len(lines[0])


def move(pos, direction_idx):
    return ((pos[0] + directions[direction_idx][0], pos[1] + directions[direction_idx][1]))


def is_valid(pos, y_max, x_max):
    y_pos, x_pos = pos
    return y_pos >= 0 and y_pos < y_max and x_pos >= 0 and x_pos < x_max


def get_adj_nodes(moves_made, direction_idx, pos, city_lines, y_max, x_max):
    adj_nodes = []
    if moves_made < MAX_MOVES:
        new_pos = move(pos, direction_idx)
        if is_valid(new_pos, y_max, x_max):
            adj_nodes.append(
                (int(city_lines[new_pos[0]][new_pos[1]]), moves_made + 1, direction_idx, new_pos))

    new_pos = move(pos, (direction_idx + 1) % len(directions))
    if is_valid(new_pos, y_max, x_max):
        adj_nodes.append((int(city_lines[new_pos[0]][new_pos[1]]), 1, (direction_idx + 1) % len(directions), new_pos))
    new_pos = move(pos, (direction_idx - 1) % len(directions))
    if is_valid(new_pos, y_max, x_max):
        adj_nodes.append((int(city_lines[new_pos[0]][new_pos[1]]), 1, (direction_idx - 1) % len(directions), new_pos))

    return adj_nodes


def solution():
    city_lines, y_max, x_max = parse_inputs(traffic_lines)
    src = (0, 0)
    root_node = (0, 0, 3, src)
    dst = (y_max - 1, x_max - 1)

    pq = []
    heapq.heappush(pq, root_node)

    distances = {}
    distances[root_node[1:]] = 0

    while len(pq) != 0:
        d, moves_made, direction_idx, pos = heapq.heappop(pq)
        curr_state = (moves_made, direction_idx, pos)
        adj_nodes = get_adj_nodes(
            moves_made, direction_idx, pos, city_lines, y_max, x_max)
        
        if pos == dst:
            target = curr_state
            break

        for weight, new_moves_made, new_direction_idx, new_pos in adj_nodes:
            new_state = (new_moves_made, new_direction_idx, new_pos)
            if new_state not in distances or distances[new_state] > distances[curr_state] + weight:
                distances[new_state] = distances[curr_state] + weight
                # found new shortest weighted path
                heapq.heappush(pq, (distances[new_state], *new_state))

    return distances[target]


print(solution())
