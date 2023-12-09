from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
history_lines = input_file.readlines()


def parse_inputs(lines):
    sequences = []
    for line in lines:
        line = line.strip()
        sequence = list(map(lambda n: int(n), line.split(' ')))
        sequences.append(sequence)
    return sequences


def is_all_zeros(sequence):
    for n in sequence:
        if n != 0:
            return False

    return True


def get_next_pattern(sequence):
    next_pattern = []
    for i in range(1, len(sequence)):
        next_pattern.append(sequence[i] - sequence[i - 1])
    return next_pattern


def get_next_n(patterns):
    curr_n = 0
    for i in range(1, len(patterns)):
        curr_n += patterns[i][-1]
    return curr_n


def solution():
    nums = []
    sequences = parse_inputs(history_lines)
    for seq in sequences:
        patterns = [seq]
        curr_pattern = patterns[0]
        while not is_all_zeros(curr_pattern):
            next_pattern = get_next_pattern(curr_pattern)
            patterns = [next_pattern] + patterns
            curr_pattern = next_pattern

        nums.append(get_next_n(patterns))

    return sum(nums)


print(solution())
