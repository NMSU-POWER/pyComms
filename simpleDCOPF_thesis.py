# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# September 2021
# simpleDCOPF_thesis.py
# Example DCOPF and other algorithms used in thesis DCOPF chapter.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpConstraint

gens = [LpVariable(name="g1", lowBound=0, upBound=150),
        LpVariable(name='g2', lowBound=0, upBound=150),
        LpVariable(name='g3', lowBound=0, upBound=150)]

costs = [1, 1.5, 2]
cost_const = 14.6

load = 400

problem = LpProblem(sense=LpMinimize)
problem += lpSum([costs[i] * gens[i] for i in range(len(gens))]) + cost_const

flows = [LpVariable('f1', lowBound=-200, upBound=200),
         LpVariable('f2', lowBound=-150, upBound=150),
         LpVariable('f3', lowBound=-150, upBound=150)]

deltas = [LpVariable('d1'),
          LpVariable('d2'),
          LpVariable('d3')]

X = [.0175, .015, .02]

problem += flows[0] == -1/X[0] * (deltas[0] - deltas[1])
problem += flows[1] == -1/X[1] * (deltas[0] - deltas[2])
problem += flows[2] == -1/X[2] * (deltas[1] - deltas[2])

lmp1 = LpConstraint(e=gens[0] - flows[0] - flows[1], rhs=0)
problem += lmp1
lmp2 = LpConstraint(e=gens[1] + flows[0] - flows[2], rhs=0)
problem += lmp2
lmp3 = LpConstraint(e=gens[2] + flows[1] + flows[2], rhs=400)
problem += lmp3

problem += deltas[0] == 0

print(problem)
problem.solve()

print(flows[0].value())
print(flows[1].value())
print(flows[2].value())
print()
print(gens[0].value())
print(gens[1].value())
print(gens[2].value())
print()
print(lmp1.pi)
print(lmp2.pi)
print(lmp3.pi)
