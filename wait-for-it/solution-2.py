from pathlib import Path
import math
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
race_lines = input_file.readlines()

# time_held as x
# time_total as t
# race goal as g
# (t - x)x > g
# solving for x
# -x^2 + tx - g = 0
# x = (-t +- sqrt(t^2 - 4(-1)(-g))) / -2


def parse_inputs(lines):
    time = lines[0].strip().split('Time:')[1]
    time = filter(lambda t: t != '', time.split(' '))
    time = int(''.join(time))
    distance = lines[1].strip().split('Distance:')[1]
    distance = filter(lambda d: d != '', distance.split(' '))
    distance = int(''.join(distance))

    return time, distance


def solution():
    time, distance = parse_inputs(race_lines)

    bound_one = (-time + math.sqrt(math.pow(time, 2) - (4 * distance)) / -2)
    bound_two = (-time - math.sqrt(math.pow(time, 2) - (4 * distance)) / -2)

    return math.ceil(bound_two - bound_one)


print(solution())
