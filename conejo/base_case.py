# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# August 2021
# base_case.py
# Solve the base case optimization, mostly so we can ensure that we have the proper result from the distributed version.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pandas
import pandas as pd
from pulp import LpProblem, LpMinimize, lpSum, LpVariable, LpConstraint, LpConstraintGE, LpConstraintLE

busses_in_one = 24
busses_in_two = 24
busses_in_three = 25

def calc_bus(from_, to_):
    from_bus = from_
    to_bus = to_
    if from_bus < 200:
        from_bus = from_bus % 100
    elif from_bus < 300:
        from_bus = from_bus % 100 + busses_in_one
    else:
        from_bus = from_bus % 100 + busses_in_one + busses_in_two
    if to_bus < 200:
        to_bus = to_bus % 100
    elif to_bus < 300:
        to_bus = to_bus % 100 + busses_in_one
    else:
        to_bus = to_bus % 100 + busses_in_one + busses_in_two
    return from_bus, to_bus

# Problem container
problem = LpProblem(name='base_case', sense=LpMinimize)

# Let's load the data and see what we have first.
f_name = 'formatted_data_linemod.xlsx'
gens = pandas.read_excel(f_name, 'gens')
lines = pandas.read_excel(f_name, 'lines')
buses = pandas.read_excel(f_name, 'busses')

# We have data loaded, now we need to build our basic model
# Objective: minimize cost of power produced
gen_costs = gens['IC']
gen_ID = gens['ID #']
gen_min = gens['Pmin']
gen_max = gens['Pmax']
gen_bus = gens['Bus #']
gen_cost_mod = gens['genCostFactor']
gen_vars = []
for i in range(len(gen_ID)):
    gen_vars.append(LpVariable('gen_' + str(gen_ID[i]), lowBound=gen_min[i], upBound=gen_max[i]))
problem += lpSum([gen_costs[i] * gen_vars[i] for i in range(len(gen_ID))])

# First constraint, sum of loads must equal sum of power.
loads = buses['MW Load']
bus_number = buses['Bus #']
theta = []
for i in range(len(loads)):
    theta.append(LpVariable('bus_' + str(i)))
# problem += lpSum(gen_vars) == sum(loads)
problem += theta[0] == 0

# Let's get the flow limits set up
flow_lim = lines['Conv MVA']
line_X = lines['X pu']
line_to = lines['To Bus']
line_from = lines['From Bus']
flow_vars = []
line_cap_constraint_low = []
line_cap_constraint_high = []
for i in range(len(flow_lim)):
    # flow_vars.append(LpVariable('flow_' + str(i), lowBound=-flow_lim[i], upBound=flow_lim[i]))
    flow_vars.append(LpVariable('flow_' + str(i)))
    line_cap_constraint_low.append(LpConstraint(e=flow_vars[i], rhs=-1 * flow_lim[i] * .9, sense=LpConstraintGE))
    line_cap_constraint_high.append(LpConstraint(e=flow_vars[i], rhs=flow_lim[i] * .9, sense=LpConstraintLE))
    problem += line_cap_constraint_low[i]
    problem += line_cap_constraint_high[i]

# We have B and a method for converting bus # to B matrix number.
# Now we need to use the to/from busses for build the flow constraints
line_constraints = []
for i in range(len(flow_vars)):
    from_bus, to_bus = calc_bus(line_from[i], line_to[i])
    constraint = LpConstraint(
        e=-100 / line_X[i] * (theta[to_bus - 1] - theta[from_bus - 1]) - flow_vars[i],
        rhs=0)
    problem += constraint
    line_constraints.append(constraint)
    # problem += -1/line_X[i] * (theta[from_bus - 1] - theta[to_bus - 1]) - flow_vars[i] == 0

# Now we can form the proper power balance constraints
# For every bus...
bus_constraints = []
for i in range(len(bus_number)):
    # We need to know all generators on bus
    gens_on_bus = []
    for j in range(len(gen_bus)):
        if gen_bus[j] == bus_number[i]:
            gens_on_bus.append(gen_vars[j])
    lines_in = []
    for j in range(len(line_to)):
        if line_to[j] == bus_number[i]:
            lines_in.append(flow_vars[j])
    lines_out = []
    for j in range(len(line_from)):
        if line_from[j] == bus_number[i]:
            lines_out.append(flow_vars[j])
    # Need handles to this constraint
    constraint = LpConstraint(e=lpSum(lines_in) + lpSum(gens_on_bus) - lpSum(lines_out), rhs=loads[i])
    problem += constraint
    bus_constraints.append(constraint)

# Solve the problem
problem.solve()

# Data dump
excel = pd.ExcelWriter('output_test.xlsx')
gen_prods = []
for i in range(len(gen_vars)):
    gen_prods.append(gen_vars[i].value())
pd.DataFrame({'limit': gen_max, 'production': gen_prods},
             columns=['limit', 'production']).to_excel(excel, sheet_name='gens')
line_loads = []
line_shadow = []
line_flow_low = []
line_flow_high = []
for i in range(len(flow_vars)):
    line_loads.append(flow_vars[i].value())
    line_shadow.append(line_constraints[i].pi)
    line_flow_low.append(line_cap_constraint_low[i].pi)
    line_flow_high.append(line_cap_constraint_high[i].pi)
pd.DataFrame({'limit': flow_lim, 'flow_loads': line_loads,
              'susceptance_shadow': line_shadow,
              'flow_low_shadow': line_flow_low,
              'flow_high_shadow': line_flow_high},
             columns=['limit', 'flow_loads', 'susceptance_shadow',
                      'flow_low_shadow', 'flow_high_shadow']).to_excel(excel, sheet_name='lines')
lmp_list = []
theta_vals = []
for i in range(len(loads)):
    lmp_list.append(bus_constraints[i].pi)
    theta_vals.append(theta[i].value())
pd.DataFrame({'bus_lmp': lmp_list, 'node_theta': theta_vals},
             columns=['bus_lmp', 'node_theta']).to_excel(excel, sheet_name='bus')
excel.close()
