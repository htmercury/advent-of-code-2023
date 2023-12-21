from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
scratch_cards = input_file.readlines()

# n, w, s, e
directions = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1)
]

steps_needed = 26501365

def parse_inputs(lines):
    rocks = set()
    for y_idx, line in enumerate(lines):
        line = line.strip()
        for x_idx, spot in enumerate(line):
            if spot == '#':
                rocks.add((y_idx, x_idx))
            elif spot == 'S':
                start = (y_idx, x_idx)
    
    return start, rocks, len(lines), len(lines[0].strip())

def solution():
    start, rocks, y_max, x_max = parse_inputs(scratch_cards)
    
    results = {
        0: set([start])
    }
    
    output = 0
    quadratic_outputs = []
    
    for steps_walked in range(steps_needed):
        results[steps_walked + 1] = set()
        for curr_pos in results[steps_walked]:
            for dy, dx in directions:
                curr_y, curr_x = curr_pos
                signed_pos = ((curr_y + dy) % y_max, (curr_x + dx) % x_max)
                new_pos = (curr_y + dy, curr_x + dx)
                if signed_pos not in rocks:
                    results[steps_walked + 1].add(new_pos)
                    
        if (steps_walked - 1) % y_max == steps_needed % y_max:
            # print(steps_walked - 1, len(results[steps_walked - 1]), len(results[steps_walked - 1]) - output, steps_walked // y_max)
            output = len(results[steps_walked - 1])
            quadratic_outputs.append(output)
            
        if len(quadratic_outputs) == 3:
            break
                        
    # print(steps_needed // y_max, steps_needed % y_max)
    
    f = lambda n,a,b,c: a + n*(b-a) + n*(n-1)//2*((c-b) - (b-a))
                    
    return f(steps_needed // y_max, *quadratic_outputs)
        

print(solution())
