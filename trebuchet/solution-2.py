from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
doc_lines = input_file.readlines()

numerical_strings = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
]


def parse_inputs(lines):
    calibration_list = []
    for line in lines:
        digit_pos = {}
        for idx, num_str in enumerate(numerical_strings):
            num = str(idx + 1)
            if num_str in line:
                first_occur = line.find(num_str)
                last_occur = line.rfind(num_str)
                
                digit_pos[first_occur] = num
                digit_pos[last_occur] = num
            if num in line:
                first_occur = line.find(num)
                last_occur = line.rfind(num)
                
                digit_pos[first_occur] = num
                digit_pos[last_occur] = num
            
        first_digit_pos = min(digit_pos.keys())
        second_digit_pos = max(digit_pos.keys())
        
        calibration_list.append(int(digit_pos[first_digit_pos] + digit_pos[second_digit_pos]))

    return calibration_list


def solution():
    calibration_list = parse_inputs(doc_lines)
    return sum(calibration_list)


print(solution())
