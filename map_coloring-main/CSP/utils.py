import random
from copy import deepcopy


def is_consistent(graph, variable_value_pairs):
    """
        returns True if the variables that have been assigned a value so far are consistent with the constraints,
        and False otherwise.

        variable_value_pairs can be used to access any value of any variable from the variable as a key
    """
    for variable, color in variable_value_pairs.items():
        if color is not None:
            for neighbor in graph[variable]:
                if neighbor in variable_value_pairs.keys() and variable_value_pairs[neighbor] == color:
                    return False
    return True


def is_solved(graph, variable_value_pairs):
    """
        returns True if the CSP is solved, and False otherwise
    """
    return all(color is not None for color in variable_value_pairs.values())


def get_next_variable(variable_value_pairs, domains):
    """
        returns the index of the next variable from the default order of the unassinged variables
    """
    for variable, color in variable_value_pairs.items():
        if color is None:
            return variable
    return None


def get_chosen_variable(graph, variable_value_pairs, domains):
    """
        returns the next variable that is deemed the best choice by the proper heuristic
        use a second heuristic for breaking ties from the first heuristic
    """
    "MRV & degree heuristic"
    min_remaining_values = float('inf')
    chosen_variables = None
    for variable in range(len(domains)):
        if variable_value_pairs[variable] is None:
            remaining_values = len(domains[variable])
            if remaining_values < min_remaining_values:
                min_remaining_values = remaining_values
                chosen_variables = [variable]
            elif remaining_values == min_remaining_values:
                    chosen_variables.append(variable)
    chosen_variable = None
    if chosen_variables is not None:
        if len(chosen_variables) == 1:
            chosen_variable = chosen_variables[0]
        else:
            # Applying degree heuristic: Selecting the variable that is involved in the largest number of
            # constraints on other unassigned variables.
            max_degree = -1
            for variable in chosen_variables:
                degree = 0
                for neighbor in graph[variable]:
                    if variable_value_pairs[neighbor] == None:
                        degree += 1
                if degree > max_degree:
                    max_degree = degree
                    chosen_variable = variable
    return chosen_variable

def count_removed_values(graph, variable_value_pairs, domains):
    queue = []
    counter = 0
    while queue:
        variable = queue.pop()
        color = variable_value_pairs[variable]
        for neighbor in graph[variable]:
            if color in domains[neighbor] and variable_value_pairs[neighbor] != color:
                domains[neighbor].remove(color)
                counter += 1
                if len(domains[neighbor]) == 0:
                    return float('inf')
                elif len(domains[neighbor]) == 1:
                    queue.append(neighbor)
    return counter

def get_ordered_domain(graph, domains, variable, variable_value_pairs):
    """
        returns the domain of the variable after ordering its values by the proper heuristic
    """
    domains_copy = deepcopy(domains)
    for var, color in variable_value_pairs.items():
        if color is not None:
            domains_copy[variable] = [color]
    ordered_domain = []
    for value in domains[variable]:
        variable_value_pairs[variable] = value
        domains_copy[variable] = [value]
        n = count_removed_values(graph, variable_value_pairs, domains_copy)
        ordered_domain.append((value, n))
    ordered_domain = [item[0] for item in sorted(ordered_domain, key=lambda x: x[1])]
    return ordered_domain

def forward_check(graph, variable_value_pairs, domains, variable, value):
    """
        removes the value assigned to the current variable from its neighbors
        returns True if backtracking is necessary, and False otherwise
    """
    for neighbor in graph[variable]:
        if value in domains[neighbor]:
            domains[neighbor].remove(value)
            if len(domains[neighbor]) == 0:
                return True
    return False

def ac3(graph, variable_value_pairs, domains):
    """
        maintains arc-consistency
        returns True if backtracking is necessary, and False otherwise
    """
    queue = [(i, j) for i in range(len(domains)) for j in graph[i]]
    while queue:
        (xi, xj) = queue.pop(0)
        if remove_inconsistent_values(xi, xj, domains):
            for neighbor in graph[xi]:
                if (neighbor, xi) not in queue:
                    queue.append((neighbor, xi))
    for domain in domains:
        if len(domain) == 0:
            return True
    return False

def remove_inconsistent_values(xi, xj, domains):
    removed = False
    for di in domains[xi]:
        found = False
        for dj in domains[xj]:
            if di != dj:
                found = True
                break
        if not found:
            domains[xi].remove(di)
            removed = True
    return removed

def count_conflicts(graph, variable_value_pairs):
    counter = 0
    for variable, color in variable_value_pairs.items():
        if color is not None:
            for neighbor in graph[variable]:
                if color == variable_value_pairs[neighbor]:
                    counter += 1
    return counter/2    # because we have counted each conflict twice

def cause_conflict(graph, variable_value_pairs, variable):
    for neighbor in graph[variable]:
        if variable_value_pairs[variable] == variable_value_pairs[neighbor]:
            return True
    return False

def random_choose_conflicted_var(graph, variable_value_pairs):
    """
        returns a random variable that is conflicting with a constraint
    """
    conflicted_vars = [var for var in variable_value_pairs if cause_conflict(graph, variable_value_pairs, var)]
    return random.choice(conflicted_vars)

def get_chosen_value(graph, variable_value_pairs, domains, variable):
    """
        returns the value by using the proper heuristic
    """
    min_conflicts = float('inf')
    values = []
    for value in domains[variable]:
        variable_value_pairs[variable] = value
        n_conflicts = count_conflicts(graph, variable_value_pairs)
        if n_conflicts < min_conflicts:
            min_conflicts = n_conflicts
            values = [value]
        elif n_conflicts == min_conflicts:
            values.append(value)
    return random.choice(values)