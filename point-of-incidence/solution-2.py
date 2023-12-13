from functools import cache
from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
hotspring_lines = input_file.readlines()


def find_sreflected_x(pattern, y_max, x_max, left_idx, right_idx, strike_outs):
    if strike_outs > 1:
        return False
    elif left_idx < 0 or right_idx >= y_max:
        if strike_outs == 1:
            return True
        return False
    else:
        diff_count = 0
        for i in range(x_max):
            if pattern[left_idx][i] != pattern[right_idx][i]:
                diff_count += 1

        return find_sreflected_x(pattern, y_max, x_max, left_idx - 1, right_idx + 1, strike_outs + diff_count)


def find_sreflected_y(pattern, y_max, x_max, left_idx, right_idx, strike_outs):
    if strike_outs > 1:
        return False
    elif left_idx < 0 or right_idx >= x_max:
        if strike_outs == 1:
            return True
        return False
    else:
        diff_count = 0
        for i in range(y_max):
            if pattern[i][left_idx] != pattern[i][right_idx]:
                diff_count += 1
        return find_sreflected_y(pattern, y_max, x_max, left_idx - 1, right_idx + 1, strike_outs + diff_count)


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
            if (find_sreflected_x(pattern, len(pattern), len(pattern[0]), i, i + 1, 0)):
                reflected_rows.append(i + 1)

        for i in range(len(pattern[0]) - 1):
            if (find_sreflected_y(pattern, len(pattern), len(pattern[0]), i, i + 1, 0)):
                reflected_columns.append(i + 1)

    return sum(reflected_columns) + sum(reflected_rows * 100)


print(solution())
