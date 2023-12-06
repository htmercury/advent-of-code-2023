from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
race_lines = input_file.readlines()

charge_speed_per_second = 1

# time_held as x
# time_total as t
# race goal as g
# (t - x)x > g
# solving for x
# x^2 - tx - g = 0
# x = (t +- sqrt(t^2 - 4(1)(-g))) / 2


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

    times_won = 0
    goal = distance
    for charged_time in range(time + 1):
        charged_speed = charged_time * charge_speed_per_second
        distance_traveled = charged_speed * (time - charged_time)
        if distance_traveled > goal:
            times_won += 1

    return times_won


print(solution())
