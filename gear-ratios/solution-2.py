from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
schematic_lines = input_file.readlines()


def get_adjacent_pos(symbol_pos):
    y_pos, x_pos = symbol_pos
    return [
        (y_pos + 1, x_pos),
        (y_pos - 1, x_pos),
        (y_pos, x_pos + 1),
        (y_pos, x_pos - 1),
        (y_pos + 1, x_pos + 1),
        (y_pos + 1, x_pos - 1),
        (y_pos - 1, x_pos + 1),
        (y_pos - 1, x_pos - 1)
    ]


def parse_inputs(lines):
    part_number_mapping = {}
    parts_list = []
    symbol_positions = []
    curr_part_idx = 0
    for y_pos, line in enumerate(lines):
        curr_num = ''
        curr_num_pos = []
        for x_pos, char in enumerate(line.strip()):
            if char.isnumeric():
                curr_num += char
                curr_num_pos.append((y_pos, x_pos))
            else:
                if len(curr_num) > 0:
                    for pos in curr_num_pos:
                        part_number_mapping[pos] = curr_part_idx
                    curr_part_idx += 1
                    parts_list.append(int(curr_num))
                curr_num = ''
                curr_num_pos = []

                if char == '*':
                    symbol_positions.append((y_pos, x_pos))

        if len(curr_num) != 0:
            for pos in curr_num_pos:
                part_number_mapping[pos] = curr_part_idx
            curr_part_idx += 1
            parts_list.append(int(curr_num))

    return part_number_mapping, symbol_positions, parts_list


def solution():
    part_number_mapping, symbol_positions, parts_list = parse_inputs(
        schematic_lines
    )

    gear_ratio = 0

    for symbol_pos in symbol_positions:
        adj_parts = set()
        adjacent_positions = get_adjacent_pos(symbol_pos)
        for pos in adjacent_positions:
            if pos in part_number_mapping:
                adj_parts.add(part_number_mapping[pos])
        
        if len(adj_parts) == 2:
            curr_ratio = 1
            for p in adj_parts:
                curr_ratio *= parts_list[p]
            gear_ratio += curr_ratio
        

    return gear_ratio


print(solution())
