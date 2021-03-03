# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March, 2021
# node_verify.py
# run an optimization so that nodes can say if they are happy with results or not.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pulp

# From our basic optimizer, we need to make the variables dynamic.
def check_validity(buckets):
    prob = pulp.LpProblem('Nodal_feasibility', pulp.LpMinimize)
    vars = []
    for bucket in buckets.keys():
        if buckets[bucket][1] == 'node':
            vars.append(pulp.LpVariable('power_' + bucket, lowBound=buckets[bucket][2], upBound=buckets[bucket][3]))
    prob += pulp.lpSum(vars)
    prob += pulp.lpSum(vars) == 0
    status = prob.solve()
    # We now know if the system is feasible, but we need to return that value.
    return pulp.LpStatus[status]
