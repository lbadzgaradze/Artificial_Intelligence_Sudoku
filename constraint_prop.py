'''
Constraint propagation
author: Levan Badzgaradze
'''
import copy
from queue import Queue


def AC3(csp, queue=None, removals=None):
    """ AC3 (Arc Consistency 3) function makes sure that every
    enqueued pair of variable satisfies binary constraint for a given
    constraint satisfaction problem(CSP). A variable in a CSP is arc-consistent
    if every value in its domain satisfies the variable’s binary constraints.

    Input:
    csp - constraint satisfaction problem. An instance of CSP or any
    of its superclasses
    queue - tuples of variables that participate in a binary constraint
    removals - inferences accumulated from assuming var=value

    returns True if method did not encounter any inconsistencies
    returns False if the CSP is not solvable under the constraints
    """
    # creating the queue which will be enqueued with variable pairs (tuples)
    # that participate in binary constraint
    q = Queue()
    if queue is not None:
        # if queue is given as a parameter as a list
        if isinstance(queue, list):
            for arc_constraint in queue:
                q.put_nowait(arc_constraint)
        # if queue is given as a parameter as a queue
        elif isinstance(queue, Queue):
            q = queue
        else:
            raise Exception("Unsupported type for second parameter of AC3")
    else:
        # if queue is not given as a parameter
        # generating every neighbour pair and enqueuing queue
        for arc_constraint in list((var, neighbour) for var in csp.variables
                                   for neighbour in csp.neighbors[var]):
            q.put_nowait(arc_constraint)

    # continue until there are tuples left in the queue
    while not q.empty():
        # pop the the tuple from the queue
        (current, neighbour) = q.get_nowait()
        # check if domain of the current variable was pruned
        if revised(csp, current, neighbour, removals):
            # if domain was pruned to 0, there is no solution, function
            # should terminate here and return false
            if len(csp.curr_domains[current]) == 0:
                return False
            # if domain was pruned but not to 0, then neighbours of the
            # variable should be enqueued since their domains might be further
            # pruned asl well
            # set of neighbours
            neighbour_variables = copy.deepcopy(csp.neighbors[current])
            # set of neighbours excluding one that was just checked
            neighbour_variables.remove(neighbour)
            # enqueuing neighbours
            for neighbour_var in neighbour_variables:
                q.put_nowait((neighbour_var, current))
    return True


def revised(csp, current, neighbour, removals):
    """This helper method checks whether variables domains was pruned (
    returns True) or not (returns False)

    Input:
    csp - constraint satisfaction problem. An instance of CSP or any
    of its superclasses
    (current, neighbour) - pair of variables participating in a binary
    constraint
    removals - inferences accumulated from assuming var=value

    """
    revised_domain = False
    # for each value in the domain of the current
    for value in csp.choices(current):
        # satisfy_found is set to True if there exists a value in the domain
        # of the neighbour that satisfies the binary constraint
        satisfy_found = False
        # each value in the domain of the neighbour
        for second_value in csp.choices(neighbour):
            if csp.constraints(current, value, neighbour, second_value):
                satisfy_found = True
                break
        # if binary constraint is not satisfied, the domain is pruned for the
        # current
        if not satisfy_found:
            # delete value from currents domain
            csp.prune(current, value, removals)
            revised_domain = True
    return revised_domain
