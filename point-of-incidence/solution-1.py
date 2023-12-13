from functools import cache
from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
hotspring_lines = input_file.readlines()


def is_reflected_x(pattern, y_max, x_max, left_idx, right_idx):
    if left_idx < 0 or right_idx >= y_max:
        return True
    else:
        for i in range(x_max):
            if pattern[left_idx][i] != pattern[right_idx][i]:
                return False
        return is_reflected_x(pattern, y_max, x_max, left_idx - 1, right_idx + 1)


def is_reflected_y(pattern, y_max, x_max, left_idx, right_idx):
    if left_idx < 0 or right_idx >= x_max:
        return True
    else:
        for i in range(y_max):
            if pattern[i][left_idx] != pattern[i][right_idx]:
                return False
        return is_reflected_y(pattern, y_max, x_max, left_idx - 1, right_idx + 1)


def parse_inputs(lines):
    patterns = []
    curr_pattern = []
    for line in lines:
        line = line.strip()
        if len(line) != 0:
            curr_pattern.append(line)
        else:
            patterns.append(curr_pattern)
            curr_pattern = []

    patterns.append(curr_pattern)
    return patterns


def solution():
    patterns = parse_inputs(hotspring_lines)

    reflected_rows = []
    reflected_columns = []

    for pattern in patterns:
        for i in range(len(pattern) - 1):
            if (is_reflected_x(pattern, len(pattern), len(pattern[0]), i, i + 1)):
                reflected_rows.append(i + 1)

        for i in range(len(pattern[0]) - 1):
            if (is_reflected_y(pattern, len(pattern), len(pattern[0]), i, i + 1)):
                reflected_columns.append(i + 1)

    return sum(reflected_columns) + sum(reflected_rows * 100)


print(solution())
