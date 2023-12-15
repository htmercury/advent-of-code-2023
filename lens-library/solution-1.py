from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
box_lines = input_file.readlines()


def parse_inputs(lines):
    return lines[0].split(',')

def HASH_algorithm(input_str):
    curr_value = 0
    for char in input_str:
        ascii_val = ord(char)
        curr_value += ascii_val
        curr_value *= 17
        curr_value = curr_value % 256
    
    return curr_value

def solution():
    parsed_lines = parse_inputs(box_lines)
    results = list(map(lambda input_str: HASH_algorithm(input_str), parsed_lines))
    
    return sum(results)


print(solution())
