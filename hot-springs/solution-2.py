import time
from functools import cache
from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
hotspring_lines = input_file.readlines()


def parse_inputs(lines):
    def get_parsed_row(line):
        record, constraint = line.strip().split(' ')
        constraint = list(map(lambda c: int(c), constraint.split(',')))
        return (record, constraint)
    parsed_lines = list(map(lambda l: get_parsed_row(l), lines))
    return parsed_lines


@cache
def count_solutions(record, constraint, curr_idx, constraint_idx, curr_group_count):
    if curr_idx == len(record):
        if len(constraint) == constraint_idx and curr_group_count == 0:
            return 1
        elif len(constraint) - 1 == constraint_idx and constraint[constraint_idx] == curr_group_count:
            return 1
        else:
            return 0
    elif record[curr_idx] == '#':
        return count_solutions(record, constraint, curr_idx + 1, constraint_idx, curr_group_count + 1)
    elif record[curr_idx] == '.':
        if curr_group_count == 0:
            return count_solutions(record, constraint, curr_idx + 1, constraint_idx, curr_group_count)
        elif constraint_idx < len(constraint) and constraint[constraint_idx] == curr_group_count:
            return count_solutions(record, constraint, curr_idx + 1, constraint_idx + 1, 0)
        else:
            return 0
    else:
        # count both options if it is a hash or dot
        option_one = count_solutions(
            record, constraint, curr_idx + 1, constraint_idx, curr_group_count + 1)
        if curr_group_count == 0:
            option_two = count_solutions(
                record, constraint, curr_idx + 1, constraint_idx, curr_group_count)
        elif constraint_idx < len(constraint) and constraint[constraint_idx] == curr_group_count:
            option_two = count_solutions(
                record, constraint, curr_idx + 1, constraint_idx + 1, 0)
        else:
            option_two = 0

        return option_one + option_two

def solution():
    parsed_lines = parse_inputs(hotspring_lines)
    valid_solutions = 0
    for line in parsed_lines:
        record, constraint = line
        valid_solutions += count_solutions('?'.join([record] * 5), tuple(constraint) * 5, 0, 0, 0)

    return valid_solutions

print(solution())
