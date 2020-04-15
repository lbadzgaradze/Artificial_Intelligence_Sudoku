'''
Constraint propagation
'''
import copy
from queue import Queue


def AC3(csp, queue=None, removals=None):
    """ AC3 constraint propagation

    A variable in a CSP is arc-consistent if every value in its domain satisfies the variable’s binary constraints.
    """
    #creating the queue which will be enqued with
    q = Queue()
    if queue is not None:
        q = queue
    else:
        for arc_constraint in list((var, neighbour) for var in csp.variables
                                   for neighbour in csp.neighbors[var]):
            q.put_nowait(arc_constraint)

    while not q.empty():
        (current, neighbour) = q.get_nowait()
        if revised(csp, current, neighbour, removals):
            if len(csp.curr_domains[current]) == 0:
                return False
            # set of neighbours
            neighbour_variables = copy.deepcopy(csp.neighbors[current])
            neighbour_variables.remove(neighbour)
            for neighbour_var in neighbour_variables:
                q.put_nowait((neighbour_var, current))
    return True


def revised(csp, current, neighbour, removals):
    revised_domain = False
    for value in csp.choices(current):
        satisfy_found = False
        for second_value in csp.choices(neighbour):
            if csp.constraints(current, value, neighbour, second_value):
                satisfy_found = True
                break
        if not satisfy_found:
            # delete value from currents domain
            csp.prune(current, value, removals)
            revised_domain = True
    return revised_domain

    # Hints:
    # Remember that:
    #    csp.variables is a list of variables
    #    csp.neighbors[x] is the neighbors of variable x
