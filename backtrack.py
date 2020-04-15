"""
Backtracking Search Algorithm
author: Levan Badzgaradze
"""

from csp_lib.backtrack_util import (first_unassigned_variable,
                                    unordered_domain_values,
                                    no_inference)


def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    """backtracking_search is a a depth-first search that chooses values for
    one variable at a time and backtracks when a variable has no legal values
    left to assign.

    Input:
    csp - constraint satisfaction problem (CSP),
    a function handle for selecting variables,
        [I am going to be using minimum remaining values (MRV) heuristic]
    a function handle for selecting elements of a domain,
        [I am going to be using the least-constraining-value heuristic.
        It prefers the value that rules out the fewest choices for the
        neighboring variables in the constraint graph.]
    and a set of inferences, solve the CSP using backtrack search
        [I will be using MAC - maintaining arc consistency]
    """
    # calling a helper function with the empty dictionary of assignments
    return backtrack({}, csp, select_unassigned_variable, order_domain_values,
                     inference)


def backtrack(assignment, csp, select_unassigned_variable, order_domain_values,
              inference):
    """Attempt to backtrack search with current assignment
    Returns None if there is no solution.  Otherwise, the
    csp should be in a goal state.
    """
    # check if the assignment is complete, it should be returned
    if csp.goal_test(assignment):
        return assignment
    # variable is selected using minimum remaining values (MRV) heuristic
    variable = select_unassigned_variable(assignment, csp)
    # value from the domain is selected using least-constraining-value
    # heuristic
    for value in order_domain_values(variable, assignment, csp):
        # if value is consistent with the assignment is should have
        # 0 conflicts
        if csp.nconflicts(variable, value, assignment) == 0:
            # if variable is consistent, we set the value
            csp.assign(variable, value, assignment)
            # we have reduced one of the variables domain to 1 (we have
            # assigned a value), this could mean that other variables domains
            # can be pruned. We will use some kind inference function (forward
            # checking or MAC (maintaining arc consistency)) to figure out
            # if other domains can be reduced
            removals = csp.suppose(variable, value)
            inference_success = inference(csp, variable, value,
                                          assignment, removals)
            # if inferences did not show that problem is not solvable
            if inference_success:
                csp.infer_assignment()
                # recursive call now with assigned (var, value) pairs
                result = backtrack(assignment, csp,
                                   select_unassigned_variable,
                                   order_domain_values, inference)
                # if results did not fail
                if result is not None and len(result) != 0:
                    return result
        # If a value choice leads to failure (noticed either by INFERENCE or
        # by BACKTRACK), then value assignments (including those made by
        # INFERENCE) are removed from the current assignment and a new value
        # is tried in the loop above.
        csp.unassign(variable, assignment)
        csp.restore(removals)
    return {}
