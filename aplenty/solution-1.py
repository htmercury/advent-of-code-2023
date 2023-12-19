from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
workflow_lines = input_file.readlines()


def parse_inputs(lines):
    workflows = {}
    parameters_list = []
    is_workflow = True
    for line in lines:
        line = line.strip()
        
        if len(line) == 0:
            is_workflow = False
            continue
        
        if is_workflow:
            workflow_name, workflow_data = line.split('{')
            workflow_data = workflow_data[:-1]
            workflows[workflow_name] = workflow_data.split(',')
        else:
            parameters = {}
            line = line[1:-1].split(',')
            for data in line:
                var_name, var_value = data.split('=')
                parameters[var_name] = int(var_value)
            parameters_list.append(parameters)
        
    return workflows, parameters_list

def get_part_status(parameters, worksflows, workflow_name):
    if workflow_name == 'A' or workflow_name == 'R':
        return workflow_name
    
    curr_workflow = worksflows[workflow_name]
    
    for condition in curr_workflow:
        if ':' in condition:
            expression, dst = condition.split(':')
            if '>' in expression:
                target, expected = expression.split('>')
                actual = parameters[target]
                if actual > int(expected):
                    return get_part_status(parameters, worksflows, dst)
            else:
                target, expected = expression.split('<')
                actual = parameters[target]
                if actual < int(expected):
                    return get_part_status(parameters, worksflows, dst)
        else:
            return get_part_status(parameters, worksflows, condition)
    
    print(curr_workflow)

def get_parameters_value(parameters):
    return sum(parameters.values())

def solution():
    workflows, parameters_list = parse_inputs(workflow_lines)
    
    accepted_parts_value = 0
    for parameters in parameters_list:
        status = get_part_status(parameters, workflows, 'in')
        if status == 'A':
            accepted_parts_value += get_parameters_value(parameters)
    
    return accepted_parts_value


print(solution())
