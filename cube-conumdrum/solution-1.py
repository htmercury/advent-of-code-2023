from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
game_lines = input_file.readlines()

cube_type_mapping = {
    'red': 0,
    'green': 1,
    'blue': 2,
}

constraint = [12, 13, 14]


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


def is_game_possible(set_list, constraint):
    for set in set_list:
        for idx, amt in enumerate(set):
            if amt > constraint[idx]:
                return False

    return True


def parse_inputs(lines):
    result = 0
    for idx, line in enumerate(lines):
        set_list = grab_cube_sets(line.strip())
        if is_game_possible(set_list, constraint):
            result += (idx + 1)
    return result


def solution():
    game_total = parse_inputs(game_lines)
    return game_total


print(solution())
