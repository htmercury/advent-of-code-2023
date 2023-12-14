import functools
from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
dish_lines = input_file.readlines()


def visualize_rocks(cube_rocks, rounded_rocks, size):
    dish_map = [['.' for col in range(size)] for row in range(size)]

    for cr in cube_rocks:
        cy, cx = cr
        dish_map[cy][cx] = '#'
    for rr in rounded_rocks:
        ry, rx = rr
        dish_map[ry][rx] = 'O'

    for row in dish_map:
        print(''.join(row))


def parse_inputs(lines):
    lines = list(map(lambda l: l.strip(), lines))
    cube_rocks = []
    rounded_rocks = []
    for y_idx, line in enumerate(lines):
        for x_idx, item in enumerate(line):
            if item == '#':
                cube_rocks.append((y_idx, x_idx))
            elif item == 'O':
                rounded_rocks.append((y_idx, x_idx))
    return cube_rocks, rounded_rocks


def rotate_left(pos, max_size):
    y_pos, x_pos = pos
    return (x_pos, max_size - y_pos)


def custom_sort(rock_one, rock_two):
    return 1 if rock_one[0] > rock_two[0] else -1


def get_final_rocks(cube_rocks, rounded_rocks, max_size):
    rounded_rocks = sorted(
        rounded_rocks, key=functools.cmp_to_key(custom_sort))
    final_rocks = []

    dish_map = [['.' for col in range(max_size + 1)]
                for row in range(max_size + 1)]
    for c_rock in cube_rocks:
        cy, cx = c_rock
        dish_map[cy][cx] = '#'

    for r_rock in rounded_rocks:
        ry_idx, rx_idx = r_rock
        while ry_idx != 0 and dish_map[ry_idx - 1][rx_idx] == '.':
            ry_idx -= 1
        dish_map[ry_idx][rx_idx] = 'O'
        final_rocks.append((ry_idx, rx_idx))

    return final_rocks


def perform_cycle(cube_rocks, rounded_rocks, max_size):
    rounded_rocks = get_final_rocks(cube_rocks, rounded_rocks, max_size)
    for _ in range(3):
        cube_rocks = list(
            map(lambda cr: rotate_left(cr, max_size), cube_rocks))
        rounded_rocks = list(
            map(lambda rr: rotate_left(rr, max_size), rounded_rocks))
        rounded_rocks = get_final_rocks(cube_rocks, rounded_rocks, max_size)

    cube_rocks = list(map(lambda cr: rotate_left(cr, max_size), cube_rocks))
    rounded_rocks = list(
        map(lambda rr: rotate_left(rr, max_size), rounded_rocks))

    return cube_rocks, rounded_rocks


def calculate_result(rounded_rocks, y_max):
    result = 0
    for r_rock in rounded_rocks:
        result += (y_max - r_rock[0])
    return result


def solution():
    cube_rocks, rounded_rocks = parse_inputs(dish_lines)
    y_max = len(dish_lines)
    total_loops = 1000000000

    # sliding window to keep track of changes for last 10 blocks
    changes = []
    sliding_window = []
    history = {}
    for idx in range(total_loops):
        cube_rocks, rounded_rocks = perform_cycle(
            cube_rocks, rounded_rocks, y_max - 1)
        state = tuple(rounded_rocks)
        if state in history:
            # find how many states has been added since the last matched state
            cycle_length = idx - history[state]

            # check if last 10 states of the last cycle matches the current cycle
            if sliding_window == changes[-cycle_length - 10: -cycle_length]:
                break

        history[state] = idx
        changes.append(state)
        if len(sliding_window) >= 10:
            sliding_window.pop(0)
        sliding_window.append(state)

    cycle = changes[-cycle_length:]
    loops_left = (total_loops - (idx + 1)) % cycle_length

    for idx in range(loops_left):
        cube_rocks, rounded_rocks = perform_cycle(
            cube_rocks, rounded_rocks, y_max - 1)

    return calculate_result(cycle[loops_left], y_max)


print(solution())
