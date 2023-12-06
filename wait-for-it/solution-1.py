from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
race_lines = input_file.readlines()

charge_speed_per_second = 1

def parse_inputs(lines):
    times = lines[0].strip().split('Time:')[1]
    times = filter(lambda t: t != '', times.split(' '))
    times = list(map(lambda t: int(t), times))
    distances = lines[1].strip().split('Distance:')[1]
    distances = filter(lambda d: d != '', distances.split(' '))
    distances = list(map(lambda t: int(t), distances))

    return times, distances


def solution():
    times, distances = parse_inputs(race_lines)
    margin_of_error = 1
    
    for i in range(len(times)):
        times_won = 0
        goal = distances[i]
        for charged_time in range(times[i] + 1):
            charged_speed = charged_time * charge_speed_per_second
            distance_traveled = charged_speed * (times[i] - charged_time)
            if distance_traveled > goal:
                times_won += 1
        margin_of_error *= times_won
    
    return margin_of_error


print(solution())
