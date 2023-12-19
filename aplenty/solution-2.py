from pathlib import Path
from copy import copy
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
workflow_lines = input_file.readlines()

MAX_VALUE = 4000
MIN_VALUE = 1


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


def calculate_expectation_result(expectations):
    result = 1
    for expected_min, expected_max in expectations.values():
        result *= (expected_max - expected_min)

    return result


def traverse_all_paths(workflows, curr_path, workflow_name, expectations):
    if workflow_name == 'R':
        return 0
    elif workflow_name == 'A':
        return calculate_expectation_result(expectations)

    result = 0
    curr_path = curr_path + [workflow_name]
    curr_workflow = workflows[workflow_name]

    for condition in curr_workflow:
        expectations = copy(expectations)
        if ':' in condition:
            expression, dst = condition.split(':')
            if '>' in expression:
                target, expected = expression.split('>')
                expected = int(expected)
                curr_min, curr_max = expectations[target]

                if curr_min > expected:
                    result += traverse_all_paths(workflows,
                                                 curr_path, dst, expectations)
                    return result
                elif curr_max > expected + 1:
                    new_bounds = [(expected + 1, curr_max),
                                  (curr_min, expected + 1)]
                    expectations[target] = new_bounds[0]
                    result += traverse_all_paths(
                        workflows, curr_path, dst, expectations)

                    expectations[target] = new_bounds[1]
            else:
                target, expected = expression.split('<')
                expected = int(expected)
                curr_min, curr_max = expectations[target]

                if curr_max <= expected:
                    result += traverse_all_paths(workflows,
                                                 curr_path, dst, expectations)
                    return result
                elif curr_min < expected:
                    new_bounds = [(curr_min, expected),
                                  (expected, curr_max)]
                    expectations[target] = new_bounds[0]
                    result += traverse_all_paths(
                        workflows, curr_path, dst, expectations)

                    expectations[target] = new_bounds[1]
        else:
            result += traverse_all_paths(workflows,
                                         curr_path, condition, expectations)
            return result


def solution():
    workflows, _ = parse_inputs(workflow_lines)

    return traverse_all_paths(workflows, [], 'in', {
        'x': (MIN_VALUE, MAX_VALUE + 1),
        'm': (MIN_VALUE, MAX_VALUE + 1),
        'a': (MIN_VALUE, MAX_VALUE + 1),
        's': (MIN_VALUE, MAX_VALUE + 1)
    })


print(solution())
