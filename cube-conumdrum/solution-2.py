import functools
from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
game_lines = input_file.readlines()

cube_type_mapping = {
    'red': 0,
    'green': 1,
    'blue': 2,
}


def grab_cube_sets(line):
    all_sets = line.split(': ')[1]
    set_list = all_sets.split('; ')
    parsed_set_list = []
    for set in set_list:
        set_values = [0, 0, 0]
        cubes = set.split(', ')
        for cube in cubes:
            cube_data = cube.split(' ')
            set_values[cube_type_mapping[cube_data[1]]] = int(cube_data[0])
        parsed_set_list.append(set_values)

    return parsed_set_list


def get_min_constraint(set_list):
    min_constraint = [0, 0, 0]
    for set in set_list:
        for idx, amt in enumerate(set):
            if amt > min_constraint[idx]:
                min_constraint[idx] = amt

    return min_constraint


def parse_inputs(lines):
    result = 0
    for line in lines:
        set_list = grab_cube_sets(line.strip())
        min_constraint = get_min_constraint(set_list)
        set_power = functools.reduce(lambda a, b: a * b, min_constraint)
        result += set_power
    return result


def solution():
    total_power = parse_inputs(game_lines)
    return total_power


print(solution())
