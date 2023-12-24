from pathlib import Path
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

def get_coefficients(px, py, vx, vy):
    a = (vy/vx)
    b = -1
    c = a * -px + py
    return a, b, c

def within_bounds(val, min_val, max_val):
    return min_val <= val < max_val

def is_past(px, py, vx, vy, x0, y0):
    if vy < 0 and y0 > py:
        return True
    elif vy > 0 and y0 < py:
        return True
    elif vx < 0 and x0 > px:
        return True
    elif vx > 0 and x0 < px:
        return True
    
    return False

def solution():
    parsed_inputs = parse_inputs(wind_lines)
    MIN_VALUE = 200000000000000
    MAX_VALUE = 400000000000000
    
    results = 0
    matched = set()
    for i in range(len(parsed_inputs)):
        for j in range(len(parsed_inputs)):
            if i != j and (i, j) not in matched and (j, i) not in matched:
                matched.add((i, j))
                px1, py1, pz1, vx1, vy1, vz1 = parsed_inputs[i]
    
                a1, b1, c1 = get_coefficients(px1, py1, vx1, vy1)
                
                px2, py2, pz2, vx2, vy2, vz2 = parsed_inputs[j]
                a2, b2, c2 = get_coefficients(px2, py2, vx2, vy2)
                
                if a1 == a2:
                    continue # parallel
                
                # https://www.cuemath.com/geometry/intersection-of-two-lines/
                x0 = (b1*c2 - b2*c1) / (a1*b2 - a2*b1)
                y0 = (c1*a2 - c2*a1) / (a1*b2 - a2*b1)
                
                if is_past(px1, py1, vx1, vy1, x0, y0) or is_past(px2, py2, vx2, vy2, x0, y0):
                    continue
                
                if within_bounds(x0, MIN_VALUE, MAX_VALUE) and within_bounds(y0, MIN_VALUE, MAX_VALUE):
                    results += 1
                
    return results


print(solution())
