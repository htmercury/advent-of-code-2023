from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
module_lines = input_file.readlines()

LOW_PULSE = 0
HIGH_PULSE = 1

def parse_inputs(lines):
    connected_input_modules = {}
    flip_flop_modules = {}
    conjunction_modules = {}
    for line in lines:
        line = line.strip()
        src, dst = line.split(' -> ')
        dst = dst.split(', ')
        if src == 'broadcaster':
            broadcaster = dst
        else:
            connected_input_modules[src[1:]] = []
            if '%' in src:
                flip_flop_modules[src[1:]] = {
                    'dst': dst,
                    'is_on': False  # off
                }
            elif '&' in src:
                conjunction_modules[src[1:]] = {
                    'dst': dst,
                    'state': {}
                }
                
    for module_name in flip_flop_modules.keys():
        for dst_module in flip_flop_modules[module_name]['dst']:
            if dst_module not in connected_input_modules:
                continue
            connected_input_modules[dst_module].append(module_name)
    
    for module_name in conjunction_modules.keys():
        for dst_module in conjunction_modules[module_name]['dst']:
            if dst_module not in connected_input_modules:
                continue
            connected_input_modules[dst_module].append(module_name)
            
    for module_name in conjunction_modules.keys():
        for connected_module in connected_input_modules[module_name]:
            conjunction_modules[module_name]['state'][connected_module] = LOW_PULSE

    return broadcaster, flip_flop_modules, conjunction_modules

def print_status(curr_pulse, prev_module, curr_module):
    keyword = 'low'
    if curr_pulse == HIGH_PULSE:
        keyword = 'high'
    
    print(prev_module + ' -' + keyword + '-> ' + curr_module)
    
def push_button(broadcaster, flip_flop_modules, conjunction_modules):
    init_state = (LOW_PULSE, 'button', 'broadcaster')
    queue = []
    queue.append(init_state)
    
    low_pulses_sent = 0
    high_pulses_sent = 0
    
    while len(queue) != 0:
        curr_pulse, prev_module, curr_module = queue.pop(0)
        # print_status(curr_pulse, prev_module, curr_module)
        
        if curr_pulse == HIGH_PULSE:
            high_pulses_sent += 1
        else:
            low_pulses_sent += 1
        
        if curr_module == 'broadcaster':
            for dst_module in broadcaster:
                queue.append((curr_pulse, curr_module, dst_module))
        elif curr_module in flip_flop_modules:
            if curr_pulse == HIGH_PULSE:
                continue # do nothing if high pulse received
            else:
                is_on = flip_flop_modules[curr_module]['is_on']
                if not is_on:
                    flip_flop_modules[curr_module]['is_on'] = True
                    for dst_module in flip_flop_modules[curr_module]['dst']:
                        queue.append((HIGH_PULSE, curr_module, dst_module))
                else:
                    flip_flop_modules[curr_module]['is_on'] = False
                    for dst_module in flip_flop_modules[curr_module]['dst']:
                        queue.append((LOW_PULSE, curr_module, dst_module))
        elif curr_module in conjunction_modules:
            next_pulse = HIGH_PULSE
            conjunction_modules[curr_module]['state'][prev_module] = curr_pulse
            # print(curr_module, conjunction_modules[curr_module]['state'])
            if sum(conjunction_modules[curr_module]['state'].values()) == len(conjunction_modules[curr_module]['state']):
                next_pulse = LOW_PULSE
            for dst_module in conjunction_modules[curr_module]['dst']:
                queue.append((next_pulse, curr_module, dst_module))
    
    return low_pulses_sent, high_pulses_sent

def solution():
    broadcaster, flip_flop_modules, conjunction_modules = parse_inputs(
        module_lines)
    
    total_low_pulses_sent = 0
    total_high_pulses_sent = 0
    
    for _ in range(1000):
        low_pulses_sent, high_pulses_sent = push_button(broadcaster, flip_flop_modules, conjunction_modules)
        total_low_pulses_sent += low_pulses_sent
        total_high_pulses_sent += high_pulses_sent

    return total_low_pulses_sent * total_high_pulses_sent


print(solution())
