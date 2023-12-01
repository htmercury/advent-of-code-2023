from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
doc_lines = input_file.readlines()


def parse_inputs(lines):
    calibration_list = []
    for line in lines:
        for token in line:
            if token.isnumeric():
                first_digit = token
                break
        for token in reversed(line):
            if token.isnumeric():
                second_digit = token
                break
        calibration_list.append(int(first_digit + second_digit))

    return calibration_list


def solution():
    calibration_list = parse_inputs(doc_lines)
    return sum(calibration_list)


print(solution())
