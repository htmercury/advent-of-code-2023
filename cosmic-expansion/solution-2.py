from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
map_lines = input_file.readlines()


def is_free_x(x_idx, map_lines):
    for y_idx in range(len(map_lines)):
        if map_lines[y_idx][x_idx] == '#':
            return False

    return True


def is_free_y(y_idx, map_lines):
    for x_idx in range(len(map_lines[0])):
        if map_lines[y_idx][x_idx] == '#':
            return False

    return True


def parse_inputs(lines):
    galaxy_list = []
    lines = list(map(lambda line: line.strip(), lines))
    free_columns = []
    free_rows = []
    for y_idx in range(len(lines)):
        if is_free_y(y_idx, lines):
            free_rows.append(y_idx)

    for x_idx in range(len(lines[0])):
        if is_free_x(x_idx, lines):
            free_columns.append(x_idx)

    scale = 1000000
    for y_idx in range(len(lines)):
        curr_free_rows = len(list(filter(lambda r: y_idx > r, free_rows)))
        for x_idx in range(len(lines[0])):
            curr_free_columns = len(
                list(filter(lambda c: x_idx > c, free_columns))
            )
            if lines[y_idx][x_idx] == '#':
                # push rows and columns by current number of free rows and free columns above and to left of current pos
                galaxy_list.append(
                    (curr_free_rows * (scale - 1) + y_idx,
                     curr_free_columns * (scale - 1) + x_idx)
                )

    return galaxy_list


def get_path_length(src, dst):
    # taxicab distance
    return abs(src[0] - dst[0]) + abs(src[1] - dst[1])


def solution():
    galaxy_list = parse_inputs(map_lines)

    answer = 0
    for galaxy_one in range(len(galaxy_list)):
        for galaxy_two in range(galaxy_one + 1, len(galaxy_list)):
            src = galaxy_list[galaxy_one]
            dst = galaxy_list[galaxy_two]
            path_length = get_path_length(src, dst)
            answer += path_length

    return answer


print(solution())
