import pandas
import pandas as pd
from pulp import LpProblem, LpMinimize, lpSum, LpVariable, LpConstraint, LpConstraintGE, LpConstraintLE, LpConstraintEQ

gens = pandas.read_excel('formatted_data_original.xlsx', 'gens')
lines = pandas.read_excel('formatted_data_original.xlsx', 'lines')
busses = pandas.read_excel('formatted_data_original.xlsx', 'busses')

# Need a problem
problem = LpProblem(name='base_optimize', sense=LpMinimize)

# Pull in cost for each generator in gens as well as gen ID
genCost = gens['IC']
genID = gens['ID #']

# We need a variable for each generator power production
power = []
low = gens['Pmin']
high = gens['Pmax']
for i in range(len(genCost)):
    power.append(LpVariable(name='gen_' + str(genID[i]), lowBound=low[i], upBound=high[i]))

# Basic power balance:
loads = busses['MW Load']
problem += sum(loads) == lpSum(power)

# We now have the basic power balance, lets add an objective and get a basic minimization going...
costs_per_MW = []
for i in range(len(genCost)):
    costs_per_MW.append(power[i] * genCost[i])

problem += lpSum(costs_per_MW)

problem.solve()
