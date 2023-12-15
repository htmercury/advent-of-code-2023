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
    boxes = {}
    for input_str in parsed_lines:
        if input_str[-1] == '-':
            label = input_str[:-1]
            target = HASH_algorithm(label)
            if target in boxes and label in boxes[target]:
                del boxes[target][label]
        else:
            label, lens = input_str.split('=')
            target = HASH_algorithm(label)
            if target not in boxes:
                boxes[target] = {}
            boxes[target][label] = int(lens)
     
    result = 0        
    for slot in boxes.keys():
        for position, label in enumerate(boxes[slot].keys()):
            result += (slot + 1) * (position + 1) * boxes[slot][label]

    return result

print(solution())
