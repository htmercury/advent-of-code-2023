from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
floor_lines = input_file.readlines()

# n,w,s,e
directions = {
    'U': (-1, 0),
    'L': (0, -1),
    'D': (1, 0),
    'R': (0, 1),
}


def transform_input_line(line):
    dir_key, distance, color = line.strip().split(' ')
    return (dir_key, int(distance), color[1:-1])


def parse_inputs(lines):
    lines = list(map(lambda l: transform_input_line(l), lines))
    return lines


def move(pos, direction_idx, distance=1):
    return (pos[0] + directions[direction_idx][0] * distance, pos[1] + directions[direction_idx][1] * distance)


def solution():
    input_lines = parse_inputs(floor_lines)
    start = (0, 0)
    vertices = [start]

    perimeter = 0
    curr_pos = start
    for dir_key, distance, _ in input_lines:
        perimeter += distance
        new_pos = move(curr_pos, dir_key, distance)
        vertices.append(new_pos)
        curr_pos = new_pos

    interior_area = 0
    i = 1
    while i < len(vertices):
        pos_one = vertices[i - 1]
        pos_two = vertices[i]
        # shoelace formula
        interior_area += (pos_one[1] * pos_two[0] - pos_one[0] * pos_two[1])

        i += 1

    interior_area = interior_area // 2
    # picks theorem
    return interior_area + perimeter // 2 + 1


print(solution())
