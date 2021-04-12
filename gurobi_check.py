# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# April 2021
# gurobi_check.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import gurobipy as gp
from gurobipy import GRB

model = gp.Model('three_bus_check')

flows = model.addVars(3, vtype=GRB.CONTINUOUS, name='flow')

power = model.addVars(3, vtype=GRB.CONTINUOUS, name='power')

angles = model.addVars(3, vtype=GRB.CONTINUOUS, name='delta', lb=float('-inf'))

load = 400

B = [-1/.017499, -1/.015001, -1/.020002]

# Basic balance, use Dr. Wang's formula
# model.addConstr(power[0] + power[1] + power[2] == load)

# Angular constraints
model.addConstr(flows[0] - 100 * B[0] * (angles[1] - angles[0]) == 0)
model.addConstr(flows[1] - 100 * B[1] * (angles[2] - angles[0]) == 0)
model.addConstr(flows[2] - 100 * B[2] * (angles[2] - angles[1]) == 0)

# Load Constraints
cost1 = model.addConstr(power[0] - flows[0] - flows[1] == 0)
cost2 = model.addConstr(power[1] + flows[0] - flows[2] == 0)
cost3 = model.addConstr(power[2] + flows[1] + flows[2] == load)

# Hold delta bus 1 at 0
model.addConstr(angles[0] == 0)

model.setObjective(power[0] * power[0] * .005 + power[0] + power[1] * power[1] * .0075 + power[1] + power[2] * power[2]
                   * .01 + power[2], GRB.MINIMIZE)

model.optimize()

print(power)

print(flows)

print(angles)

print(cost1.Pi)

print(cost2.Pi)

print(cost3.Pi)
