import pandas
import pandas as pd
from pulp import LpProblem, LpMinimize, lpSum, LpVariable, LpConstraint, LpConstraintGE, LpConstraintLE, LpConstraintEQ

problem = LpProblem(name='b-theta', sense=LpMinimize)

f_name = 'a.xlsx'
gens = pandas.read_excel(f_name, 'gens')
lines = pandas.read_excel(f_name, 'lines')
buses = pandas.read_excel(f_name, 'busses')
splices = pandas.read_excel(f_name, 'splice_lines')

Betas = [106.6896333, 100.132514]
Gammas = [105.7097067, 99.224348]

# Bring in generator restrictions and the objective
gen_vars = []
for i in range(len(gens['ID #'])):
    gen_vars.append(LpVariable('gen'+str(i), lowBound=0, upBound=gens['Pmax'][i]))
# problem += lpSum([gen_vars[i] * gens['IC'][i] for i in range(len(gens['ID #']))])

# We need theta for every node
bus_keys = {}
theta = []
for i in range(len(buses['Bus #'])):
    bus_keys[buses['Bus #'][i]] = i
    theta.append(LpVariable('theta'+str(buses['Bus #'][i])))

# We need internal flow constraints
B = []
flowgate = []
for i in range(len(lines['ID #'])):
    B.append(-1/lines['X pu'][i])
    low = LpConstraint(e=-B[i]*(theta[bus_keys[lines['To Bus'][i]]] - theta[bus_keys[lines['From Bus'][i]]]),
                       rhs=-lines['Conv MVA'][i]*.9, sense=LpConstraintGE)
    high = LpConstraint(e=-B[i]*(theta[bus_keys[lines['To Bus'][i]]] - theta[bus_keys[lines['From Bus'][i]]]),
                        rhs=lines['Conv MVA'][i]*.9, sense=LpConstraintLE)
    flowgate.append((low, high))
    problem += low
    problem += high

# We need tie thetas
thetay = []
# thetaz = []
Btie = []
for i in range(len(splices['ID #'])):
    Btie.append(-1/splices['X pu'][i])
    thetay.append(LpVariable(name='thetay'+splices['ID #'][i]))
    # thetaz.append(LpVariable(name='thetaz'+splices['ID #'][i]))

# Bring in generator restrictions and the objective
gen_vars = []
for i in range(len(gens['ID #'])):
    gen_vars.append(LpVariable('gen'+str(i), lowBound=0, upBound=gens['Pmax'][i]))
problem += lpSum([gen_vars[i] * gens['IC'][i] for i in range(len(gens['ID #']))]) - \
           lpSum([Betas[i] * (3*Btie[i]*(theta[bus_keys[splices['From Bus'][i]]] -
                                         (2*Betas[i]-Gammas[i])/Betas[i]*thetay[i])) for i in range(len(splices['ID #']))])

# We need to make the tie flow limits
# Y side first
flowgatey = []
for i in range(len(splices['ID #'])):
    low = LpConstraint(e=-3 * Btie[i] * (theta[bus_keys[splices['From Bus'][i]]] - thetay[i]),
                       rhs=-splices['Conv MVA'][i]*.9, sense=LpConstraintGE)
    high = LpConstraint(e=-3 * Btie[i] * (theta[bus_keys[splices['From Bus'][i]]] - thetay[i]),
                        rhs=splices['Conv MVA'][i]*.9, sense=LpConstraintLE)
    flowgatey.append((low, high))
    problem += low
    problem += high
# Z side now
'''flowgatez = []
for i in range(len(splices['ID #'])):
    low = LpConstraint(e=3 * Btie[i]*(theta[bus_keys[splices['To Bus'][i]]] - thetaz[i]),
                       rhs=-splices['Conv MVA'][i]*.9, sense=LpConstraintGE)
    high = LpConstraint(e=3 * Btie[i] * (theta[bus_keys[splices['To Bus'][i]]] - thetaz[i]),
                        rhs=splices['Conv MVA'][i]*.9, sense=LpConstraintLE)
    flowgatez.append((low, high))
    problem += low
    problem += high'''

# Beta/Gamma constraints
'''Betas = []
Gammas = []
for i in range(len(splices['ID #'])):
    Betas.append(LpConstraint(3 * Btie[i] * (theta[bus_keys[splices['From Bus'][i]]] - thetay[i]) + 3 * Btie[i] * (thetaz[i] - thetay[i])))
    Gammas.append(LpConstraint(3 * Btie[i] * (theta[bus_keys[splices['To Bus'][i]]] - thetaz[i]) + 3 * Btie[i] * (thetay[i] - thetaz[i])))
    problem += Betas[i]
    problem += Gammas[i]'''

# LMP Data Gather
lmp = []
for i in range(len(buses['Bus #'])):
    gen_on_bus = []
    incoming_lines = []
    outgoing_lines = []
    tie_lines = []
    for j in range(len(gens['Bus #'])):
        if buses['Bus #'][i] == gens['Bus #'][j]:
            gen_on_bus.append(gen_vars[j])
    for j in range(len(lines['ID #'])):
        if buses['Bus #'][i] == lines['To Bus'][j]:
            incoming_lines.append(-B[j] * (theta[bus_keys[buses['Bus #'][i]]] - theta[bus_keys[lines['From Bus'][j]]]))
    for j in range(len(lines['ID #'])):
        if buses['Bus #'][i] == lines['From Bus'][j]:
            outgoing_lines.append(-B[j] * (theta[bus_keys[lines['To Bus'][j]]] - theta[bus_keys[buses['Bus #'][i]]]))
    for j in range(len(splices['ID #'])):
        if buses['Bus #'][i] == splices['From Bus'][j]:
            tie_lines.append(3 * Btie[j] * (theta[bus_keys[buses['Bus #'][i]]] - thetay[j]))
    '''for j in range(len(splices['ID #'])):
        if buses['Bus #'][i] == splices['To Bus'][j]:
            tie_lines.append(3 * Btie[j] * (theta[bus_keys[buses['Bus #'][i]]] - thetaz[j]))'''
    lmp.append(LpConstraint(e=lpSum(gen_on_bus) + lpSum(incoming_lines) - lpSum(outgoing_lines) - lpSum(tie_lines),
                            rhs=buses['MW Load'][i], sense=LpConstraintEQ))
    problem += lmp[i]

problem += theta[0] == 0

problem.solve()

# Data dump
excel = pd.ExcelWriter('output.xlsx')
gen_prods = []
gen_max = []
for i in range(len(gen_vars)):
    gen_prods.append(gen_vars[i].value())
    gen_max.append(gens['Pmax'][i])
pd.DataFrame({'limit': gen_max, 'production': gen_prods},
             columns=['limit', 'production']).to_excel(excel, sheet_name='gens')

flows = []
flowgates = []
limits = []
to = []
froms = []
for i in range(len(lines['ID #'])):
    to.append(lines['To Bus'][i])
    froms.append(lines['From Bus'][i])
    limits.append(lines['Conv MVA'][i])
    flows.append(-B[i] * (theta[bus_keys[lines['To Bus'][i]]].value() - theta[bus_keys[lines['From Bus'][i]]].value()))
    flowgates.append(flowgate[i][0].pi + flowgate[i][1].pi)
pd.DataFrame({'to': to, 'from': froms, 'limits': limits, 'Flow': flows, 'flowgates': flowgates},
             columns=['to', 'from', 'limits', 'Flow', 'flowgates']).to_excel(excel, sheet_name='lines_internal')

flows_outer = []
flowgatesy = []
flowgatesz = []
limits = []
to = []
froms = []
beta_vals = []
gamma_vals = []
for i in range(len(splices['ID #'])):
    to.append(splices['To Bus'][i])
    froms.append(splices['From Bus'][i])
    limits.append(splices['Conv MVA'][i])
    flows_outer.append(B[i] * (theta[bus_keys[splices['From Bus'][i]]].value() - thetay[i].value()))
    flowgatesy.append(flowgatey[i][0].pi + flowgatey[i][1].pi)
    flowgatesz.append(0)
    beta_vals.append(0)
    gamma_vals.append(0)
pd.DataFrame({'from': froms, 'to': to, 'limits': limits, 'Flow': flows_outer, 'flowgatesy': flowgatesy, 'flowgatesz': flowgatesz, 'beta': beta_vals, 'gamma': gamma_vals},
             columns=['from', 'to', 'limits', 'Flow', 'flowgatesy', 'flowgatesz', 'beta', 'gamma']).to_excel(excel, sheet_name='lines_splice')

lmp_vals = []
node = []
angles = []
for i in range(len(buses['Bus #'])):
    lmp_vals.append(lmp[i].pi)
    node.append(buses['Bus #'][i])
    angles.append(theta[i].value())
pd.DataFrame({'bus': node, 'lmp': lmp_vals, 'theta': angles},
             columns=['bus', 'lmp', 'theta']).to_excel(excel, sheet_name='buses')

excel.close()
