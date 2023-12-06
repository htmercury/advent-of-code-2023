from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
almanac_lines = input_file.readlines()


def parse_seeds(seeds):
    results = []
    seeds = iter(seeds)
    for s in seeds:
        results.append((s, s + next(seeds) - 1))

    return results


def get_overlap(pair_one, pair_two):
    return (max(pair_one[0], pair_two[0]), min(pair_one[1], pair_two[1]))


def get_underlap(pair_one, pair_two):
    results = []
    if pair_one[0] < pair_two[0]:
        results.append((pair_one[0], pair_two[0] - 1))
    if pair_one[1] > pair_two[1]:
        results.append((pair_two[1] + 1, pair_one[1]))

    return results


def is_valid(pair):
    return pair[1] >= pair[0]


def transform(seed_pairs, map_data):
    transformed_seeds = []

    i = 0
    while i < len(seed_pairs):
        seed_pair = seed_pairs[i]
        for src_dest_category in map_data:
            dest = src_dest_category[0]
            src = src_dest_category[1]
            r_length = src_dest_category[2]

            overlap = get_overlap(seed_pair, (src, src + r_length - 1))
            if is_valid(overlap):
                transformed_seeds.append(
                    (overlap[0] - src + dest, overlap[1] - src + dest))
                remaining_seeds = get_underlap(
                    seed_pair, (src, src + r_length - 1))
                seed_pairs += remaining_seeds
                break
        else:
            transformed_seeds.append(seed_pair)
        i += 1

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
    seed_pairs = parse_seeds(seeds)
    for map_data in maps_data:
        seed_pairs = transform(seed_pairs, map_data)
    return min(map(lambda s: s[0], seed_pairs))


print(solution())
