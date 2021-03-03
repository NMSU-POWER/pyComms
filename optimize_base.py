import pulp

prob = pulp.LpProblem('Nodal_feasibility', pulp.LpMinimize)

# Actual power net injection:
P1_act = 184.615
P2_act = 123.077
P3_act = -307.692

# 5MW buckets to start with
P1 = pulp.LpVariable('Power_one', lowBound=184.615, upBound=184.615)
P2 = pulp.LpVariable('Power_two', lowBound=100, upBound=150)
P3 = pulp.LpVariable('Power_three', lowBound=-350, upBound=-300)

# The soaking dummy
# P4 = pulp.LpVariable('Power_off', lowBound=0, upBound=5)

# Objective from node 1's perspective:
prob += P1 + P2 + P3

# Constraint:
prob += P1 + P2 + P3 == 0

# Solve:
status = prob.solve()

print(P1.value())
print(P2.value())
print(P3.value())
print()
print(P1.value() - P1_act)
print(P2.value() - P2_act)
print(P3.value() - P3_act)
print(pulp.LpStatus[status])
