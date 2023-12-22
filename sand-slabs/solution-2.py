import heapq
from functools import cache
import re
import collections
import itertools as it
from copy import copy, deepcopy
from pathlib import Path
import time
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
brick_lines = input_file.readlines()


def parse_inputs(lines):
    bricks = {}
    curr_brick_id = 65
    x_max = y_max = z_max = 0
    for ranges in lines:
        ranges = ranges.strip()
        pos_one, pos_two = ranges.split('~')
        pos_one = tuple(map(lambda p: int(p), pos_one.split(',')))
        pos_two = tuple(map(lambda p: int(p), pos_two.split(',')))
        bricks[chr(curr_brick_id)] = (pos_one, pos_two)

        x_max = max(pos_one[0], pos_two[0], x_max)
        y_max = max(pos_one[1], pos_two[1], y_max)
        z_max = max(pos_one[2], pos_two[2], z_max)

        curr_brick_id += 1

    return bricks, x_max, y_max, z_max


def visualize_x(bricks, x_max, z_max):
    bricks_map = [['.' for col in range(x_max + 1)]
                  for row in range(z_max + 1)]
    for brick_name in bricks.keys():
        pos_one, pos_two = bricks[brick_name]
        x_magnitude = abs(pos_two[0] - pos_one[0] + 1)
        x_start = min(pos_one[0], pos_two[0])

        z_magnitude = abs(pos_two[2] - pos_one[2] + 1)
        z_start = min(pos_one[2], pos_two[2])
        for j in range(z_start, z_start + z_magnitude):
            for i in range(x_start, x_start + x_magnitude):
                if bricks_map[z_max - j][i] == '.':
                    bricks_map[z_max - j][i] = brick_name
                else:
                    bricks_map[z_max - j][i] = '?'

    for i in range(x_max + 1):
        bricks_map[z_max][i] = '-'
    for _ in bricks_map:
        print(''.join(_))


def visualize_y(bricks, y_max, z_max):
    bricks_map = [['.' for col in range(y_max + 1)]
                  for row in range(z_max + 1)]
    for brick_name in bricks.keys():
        pos_one, pos_two = bricks[brick_name]
        y_magnitude = abs(pos_two[1] - pos_one[1] + 1)
        y_start = min(pos_one[1], pos_two[1])

        z_magnitude = abs(pos_two[2] - pos_one[2] + 1)
        z_start = min(pos_one[2], pos_two[2])
        for j in range(z_start, z_start + z_magnitude):
            for i in range(y_start, y_start + y_magnitude):
                if bricks_map[z_max - j][i] == '.':
                    bricks_map[z_max - j][i] = brick_name
                else:
                    bricks_map[z_max - j][i] = '?'

    for i in range(y_max + 1):
        bricks_map[z_max][i] = '-'
    for _ in bricks_map:
        print(''.join(_))


def get_brick_pts(pos_one, pos_two):
    results = set()
    x_magnitude = abs(pos_two[0] - pos_one[0] + 1)
    x_start = min(pos_one[0], pos_two[0])
    y_magnitude = abs(pos_two[1] - pos_one[1] + 1)
    y_start = min(pos_one[1], pos_two[1])
    z_magnitude = abs(pos_two[2] - pos_one[2] + 1)
    z_start = min(pos_one[2], pos_two[2])
    for k in range(z_start, z_start + z_magnitude):
        for j in range(y_start, y_start + y_magnitude):
            for i in range(x_start, x_start + x_magnitude):
                results.add((i, j, k))

    return results


def move_bricks(pq, bricks):
    fixed_pts = set()
    bricks_labeled_pts = {}
    while len(pq) != 0:
        height, brick_name, (pos_one, pos_two) = heapq.heappop(pq)
        brick_pos_list = get_brick_pts(pos_one, pos_two)
        while height > 1:
            # check if brick is free
            is_free = True
            new_pos_list = []
            for b_x, b_y, b_z in brick_pos_list:
                if (b_x, b_y, b_z - 1) in fixed_pts:
                    is_free = False  # collison
                else:
                    new_pos_list.append((b_x, b_y, b_z - 1))

            if is_free:
                height -= 1
                # print(brick_name, ' falls one down to height ', height)
                pos_one = (pos_one[0], pos_one[1], pos_one[2] - 1)
                pos_two = (pos_two[0], pos_two[1], pos_two[2] - 1)
                brick_pos_list = new_pos_list
            else:
                break

        fixed_pts.update(brick_pos_list)
        bricks_labeled_pts[brick_name] = brick_pos_list

        # update original bricks
        bricks[brick_name] = (pos_one, pos_two)

    return bricks_labeled_pts


def solution():
    bricks, x_max, y_max, z_max = parse_inputs(brick_lines)

    brick_supporting = {}
    brick_supported_by = {}

    pq = []
    for brick_name in bricks.keys():
        pos_one, pos_two = bricks[brick_name]
        z_min = min(pos_one[2], pos_two[2])
        heapq.heappush(pq, (z_min, brick_name, bricks[brick_name]))

        brick_supporting[brick_name] = set()
        brick_supported_by[brick_name] = set()

    placements = move_bricks(pq, bricks)
    
    # visualize_x(bricks, x_max, z_max)
    # visualize_y(bricks, y_max, z_max)

    for target_brick in bricks.keys():
        for brick_name in bricks.keys():
            pos_one, pos_two = bricks[brick_name]
            z_min = min(pos_one[2], pos_two[2])
            if target_brick != brick_name and z_min > 1:
                for (px, py, pz) in placements[brick_name]:
                    if (px, py, pz - 1) in placements[target_brick]:
                        brick_supporting[target_brick].add(brick_name)
                        brick_supported_by[brick_name].add(target_brick)

    results = 0
    for target_brick in bricks.keys():
        # simulate entire fall if this targeted brick is deleted
        queue = [target_brick]
        fall = set([target_brick])

        while len(queue) != 0:
            falling_bricks = queue.pop()
            # get bricks that should have fallen as well
            for supporting_bricks in brick_supporting[falling_bricks]:
                # check what bricks do those fallen bricks support
                supported_bricks = brick_supported_by[supporting_bricks]

                # these bricks would fall accordingly if all its dependencies has already fallen
                if supported_bricks.issubset(fall):
                    fall.add(supporting_bricks)
                    queue.append(supporting_bricks)

        fall.remove(target_brick)  # delete the brick
        results += len(fall)

    return results


print(solution())
