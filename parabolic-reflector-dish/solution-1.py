from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
dish_lines = input_file.readlines()


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


def solution():
    cube_rocks, rounded_rocks = parse_inputs(dish_lines)

    final_rocks = []

    for r_rock in rounded_rocks:
        ry_idx, rx_idx = r_rock
        while ry_idx != 0 and (ry_idx - 1, rx_idx) not in cube_rocks and (ry_idx - 1, rx_idx) not in final_rocks:
            ry_idx -= 1
        final_rocks.append((ry_idx, rx_idx))
    
    result = 0
    y_max = len(dish_lines)
    for f_rock in final_rocks:
        result += (y_max - f_rock[0])
    
    return result

print(solution())
