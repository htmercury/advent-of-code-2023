import re
from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
hotspring_lines = input_file.readlines()


def parse_inputs(lines):
    lines = list(map(lambda l: l.strip(), lines))
    all_unknowns = []
    for line in lines:
        unknown_positions = []
        for idx, spring_char in enumerate(line):
            if spring_char == '?':
                unknown_positions.append(idx)
        all_unknowns.append(unknown_positions)

    return lines, all_unknowns


def binary_combinations(n, memorized):
    combinations = []
    total = 2**n
    if total in memorized:
        return memorized[total]
    for i in range(total):
        res = [int(i) for i in list('{0:0b}'.format(i))]
        res = ([0] * (n - len(res))) + res
        combinations.append(res)

    memorized[total] = combinations
    return combinations


def solution():
    possibilities = ['.', '#']
    lines, all_unknowns = parse_inputs(hotspring_lines)
    valid_solutions = 0
    for idx, unknown_positions in enumerate(all_unknowns):
        print(idx)
        line = lines[idx]
        record, constraint = line.split(' ')
        constraint = constraint.split(',')
        constraint = list(map(lambda c: int(c), constraint))

        memorized = {}
        combinations = binary_combinations(len(unknown_positions), memorized)
        for combination in combinations:
            new_record = list(record)
            for guessed_idx, unknown_idx in zip(combination, unknown_positions):
                new_record[unknown_idx] = possibilities[guessed_idx]
            new_constraint = re.split(r'\.+', ''.join(new_record))
            new_constraint = filter(lambda c: len(c) != 0, new_constraint)
            new_constraint = list(map(lambda x: len(x), new_constraint))

            if new_constraint == constraint:
                valid_solutions += 1

    return valid_solutions


print(solution())
