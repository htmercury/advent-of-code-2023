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

steps_needed = 99

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
    
    root_node = (0, start, start)
    queue = []
    queue.append(root_node)
    visited = set()
    visited.add(root_node)
    
    
    results = {}
    
    while len(queue) != 0:
        dist, unsigned_pos, curr_pos = queue.pop(0)
        
        if dist not in results:
            results[dist] = set()
        
        results[dist].add(unsigned_pos)
        
        if dist > steps_needed:
            break
        else:
            for dy, dx in directions:
                curr_y, curr_x = curr_pos
                unsigned_y, unsigned_x = unsigned_pos
                new_pos = ((curr_y + dy) % y_max, (curr_x + dx) % x_max)
                new_unsigned_pos = (unsigned_y + dy, unsigned_x + dx)
                if new_pos not in rocks:
                    new_node = (dist + 1, new_unsigned_pos, new_pos)
                    if new_node not in visited:
                        queue.append(new_node)
                        visited.add(new_node)
                    
    return len(results[steps_needed])
        


print(solution())
