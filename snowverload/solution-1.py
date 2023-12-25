from pathlib import Path
import networkx as nx
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
component = input_file.readlines()


def parse_inputs(lines):
    components = set()
    dependencies = {}
    graph = nx.Graph()
    for line in lines:
        line = line.strip()
        src, data = line.split(': ')
        dst = data.split(' ')
        components.add(src)

        if src not in dependencies:
            dependencies[src] = set()

        dependencies[src] = dependencies[src] | set(dst)

        for comp in dst:
            graph.add_edge(src, comp)
            components.add(comp)
            if comp not in dependencies:
                dependencies[comp] = set()
            dependencies[comp] = dependencies[comp] | set([src])

    return components, dependencies, graph


def delete_wire(comp_one, comp_two, dependencies):
    dependencies[comp_one].remove(comp_two)
    dependencies[comp_two].remove(comp_one)


def get_group(curr_group, curr_comp, dependencies, components):
    if curr_comp in curr_group:
        return curr_group

    curr_group.add(curr_comp)
    if curr_comp in components:
        components.remove(curr_comp)

    for dependency_comp in dependencies[curr_comp]:
        curr_group = get_group(curr_group, dependency_comp,
                               dependencies, components) | curr_group

    return curr_group


def solution():
    components, dependencies, graph = parse_inputs(component)

    cuts = nx.minimum_edge_cut(graph)

    for comp_one, comp_two in cuts:
        delete_wire(comp_one, comp_two, dependencies)

    remaining_components = components.copy()
    groups = []
    while len(remaining_components) != 0:
        curr_comp = remaining_components.pop()
        curr_group = get_group(
            set(), curr_comp, dependencies, remaining_components)

        groups.append(curr_group)

    return len(groups[0]) * len(groups[1])


print(solution())
