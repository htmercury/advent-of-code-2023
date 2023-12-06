from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
almanac_lines = input_file.readlines()


def transform(seeds, map):
    transformed_seeds = []

    for seed in seeds:
        for src_dest_category in map:
            dest = src_dest_category[0]
            src = src_dest_category[1]
            r_length = src_dest_category[2]
            if src <= seed < src + r_length:
                loc = seed - src
                transformed_seeds.append(dest + loc)
                break
        else:
            transformed_seeds.append(seed)

    return transformed_seeds


def parse_inputs(lines):
    seeds = []
    data = []
    curr_maps = []
    seeds = lines[0].split('seeds: ')[1]
    seeds = list(map(lambda s: int(s), seeds.split(' ')))
    lines = lines[3:]
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        elif ':' in line:
            data.append(curr_maps)
            curr_maps = []
        else:
            curr_maps.append(list(map(lambda d: int(d), line.split(' '))))

    # last row
    data.append(curr_maps)

    return seeds, data


def solution():
    seeds, maps_data = parse_inputs(almanac_lines)
    for map in maps_data:
        seeds = transform(seeds, map)
    return min(seeds)


print(solution())
