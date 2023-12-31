from pathlib import Path
from z3 import Int, Ints, Solver
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
wind_lines = input_file.readlines()


def parse_inputs(lines):
    results = []
    for line in lines:
        line = line.strip()
        raw_data = line.split(' ')
        clean_data = []
        for value in raw_data:
            if len(value) == 0 or value == '@':
                continue
            elif value[-1] == ',':
                clean_data.append(int(value[:-1]))
            else:
                clean_data.append(int(value))
        results.append(tuple(clean_data))

    return results


def solution():
    parsed_inputs = parse_inputs(wind_lines)

    x, y, z, vx, vy, vz = Ints("x y z vx vy vz")

    s = Solver()
    for idx, hail in enumerate(parsed_inputs[:3]):
        t = Int(f"t{idx}")
        s.add(t > 0)
        pxh, pyh, pzh, vxh, vyh, vzh = hail
        s.add(x + vx * t == pxh + vxh * t)
        s.add(y + vy * t == pyh + vyh * t)
        s.add(z + vz * t == pzh + vzh * t)
    s.check()
    x = s.model()[x].as_long()
    y = s.model()[y].as_long()
    z = s.model()[z].as_long()

    return x + y + z


print(solution())
