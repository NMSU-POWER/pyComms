# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# September 2021
# Area.py
# Store problem for one area.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pandas
import pandas as pd
from pulp import LpProblem, LpMinimize, lpSum, LpVariable, LpConstraint, LpConstraintGE, LpConstraintLE


# Hold area problem for one area
class Area:
    # Initialize the area using the provided data set.
    def __init__(self, sheet_name, area):
        self.AreaNum = area
        # Let's load the data and see what we have first.
        self.data_sheet = sheet_name
        self.gens = pandas.read_excel(self.data_sheet, 'gens')
        self.lines = pandas.read_excel(self.data_sheet, 'lines')
        self.buses = pandas.read_excel(self.data_sheet, 'busses')
        self.ties = pandas.read_excel(self.data_sheet, 'splice_lines')
        self.alpha = [100] * len(self.ties['From Bus'])
        self.area = area

    def setup(self):
        # New variables
        self.problem = LpProblem(name='base_case', sense=LpMinimize)
        self.tie_theta = []
        froms = self.ties['From Bus']
        tos = self.ties['To Bus']
        tie_limits = self.ties['Conv MVA']
        self.tie_X = self.ties['X pu']
        # We now need to implement flow limits on these lines, i think...
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.tie_flow_constraints_high = []
        self.tie_flow_constraints_low = []
        self.tie_flow = []
        self.internal = []
        self.external = []
        for i in range(len(froms)):
            if froms[i] // 100 == self.lines['From Bus'][0] // 100:
                self.internal.append(froms[i])
                self.external.append(tos[i])
            else:
                self.internal.append(tos[i])
                self.external.append(froms[i])
            self.tie_theta.append(LpVariable(name='tie_'+str(self.internal[i])+' to ' + str(self.external[i])))
            self.tie_flow.append(LpVariable(name='tie_F_'+str(self.area)+':'+str(i)))
            self.tie_flow_constraints_high.append(LpConstraint(e=self.tie_flow[i], rhs=.9 * tie_limits[i],
                                                               sense=LpConstraintLE))
            self.tie_flow_constraints_low.append(LpConstraint(e=self.tie_flow[i], rhs=-.9 * tie_limits[i],
                                                              sense=LpConstraintGE))
            self.problem += self.tie_flow_constraints_low[i]
            self.problem += self.tie_flow_constraints_high[i]

        # We now have a theta for every tie line, as well as the flow variables, alpha for price and flow constraints
        # We should be completely ready to implement the new objective function.

        # We have data loaded, now we need to build our basic model
        # Objective: minimize cost of power produced
        self.gen_costs = self.gens['IC']
        gen_ID = self.gens['ID #']
        gen_min = self.gens['Pmin']
        self.gen_max = self.gens['Pmax']
        gen_bus = self.gens['Bus #']
        self.gen_vars = []
        for i in range(len(gen_ID)):
            self.gen_vars.append(LpVariable('gen_' + str(gen_ID[i]), lowBound=gen_min[i], upBound=self.gen_max[i]))
        # self.problem += lpSum([gen_costs[i] * self.gen_vars[i] for i in range(len(gen_ID))]) \
        #                 + lpSum([alpha[i] * 2 * tie_X[i] * theta])

        # First constraint, sum of loads must equal sum of power.
        self.loads = self.buses['MW Load']
        bus_number = self.buses['Bus #']
        self.theta = []
        for i in range(len(self.loads)):
            self.theta.append(LpVariable('bus_' + str(i)))

        # Let's get the flow limits set up
        self.flow_lim = self.lines['Conv MVA']
        line_X = self.lines['X pu']
        line_to = self.lines['To Bus']
        line_from = self.lines['From Bus']
        self.flow_vars = []
        self.line_cap_constraint_low = []
        self.line_cap_constraint_high = []
        for i in range(len(self.flow_lim)):
            # flow_vars.append(LpVariable('flow_' + str(i), lowBound=-flow_lim[i], upBound=flow_lim[i]))
            self.flow_vars.append(LpVariable('flow_' + str(i)))
            self.line_cap_constraint_low.append(
                LpConstraint(e=self.flow_vars[i], rhs=-1 * self.flow_lim[i] * .9, sense=LpConstraintGE))
            self.line_cap_constraint_high.append(LpConstraint(e=self.flow_vars[i], rhs=self.flow_lim[i] *
                                                                                       .9, sense=LpConstraintLE))
            self.problem += self.line_cap_constraint_low[i]
            self.problem += self.line_cap_constraint_high[i]

        self.line_constraints = []
        for i in range(len(self.flow_vars)):
            from_bus, to_bus = line_from[i] % 100, line_to[i] % 100
            constraint = LpConstraint(
                e=100 * -1 / line_X[i] * (self.theta[to_bus - 1] - self.theta[from_bus - 1]) - self.flow_vars[i],
                rhs=0)
            self.problem += constraint
            self.line_constraints.append(constraint)
        self.tie_constraints = []
        for i in range(len(self.tie_flow)):
            # if tos[i] // 100 == area:
            constraint = LpConstraint(e=100 * -2/self.tie_X[i] *
                                        (self.tie_theta[i] - self.theta[self.internal[i] % 100 - 1])
                                        - self.tie_flow[i])
            # else:
            #     constraint = LpConstraint(e=100 * -1 / self.tie_X[i] * (-self.theta[tos[i] % 100 - 1] +
            #                                                             self.tie_theta[i]) - self.tie_flow[i])
            self.tie_constraints.append(constraint)
            self.problem += constraint

        # Now we can form the proper power balance constraints
        # For every bus...
        self.bus_constraints = []
        for i in range(len(bus_number)):
            # We need to know all generators on bus
            gens_on_bus = []
            for j in range(len(gen_bus)):
                if gen_bus[j] == bus_number[i]:
                    gens_on_bus.append(self.gen_vars[j])
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Tied every bus to every output line...
            lines_in = []
            for j in range(len(line_to)):
                if line_to[j] == bus_number[i]:
                    lines_in.append(self.flow_vars[j])
            # for j in range(len(self.tie_flow)):
            #     if tos[j] // 100 == line_to[0] // 100 and tos[j] % 100 == bus_number[i]:
            #         lines_in.append(self.tie_flow[j])
            lines_out = []
            for j in range(len(line_from)):
                if line_from[j] == bus_number[i]:
                    lines_out.append(self.flow_vars[j])
            # for j in range(len(self.tie_flow)):
            #     if froms[j] // 100 == line_to[0] // 100 or froms[j] % 100 == bus_number[i]:
            #         lines_out.append(self.flow_vars[j])
            for j in range(len(self.internal)):
                # I almost hope it isn't this simple...
                # if self.internal[j] % 100 == bus_number[i]:
                if self.internal[j] == bus_number[i]:
                    lines_out.append(self.tie_flow[j])
            # Need handles to this constraint
            constraint = LpConstraint(e=lpSum(lines_in) + lpSum(gens_on_bus) - lpSum(lines_out), rhs=self.loads[i])
            self.problem += constraint
            self.bus_constraints.append(constraint)

        self.problem += lpSum([self.gen_costs[i] * self.gen_vars[i] for i in range(len(gen_ID))]) - \
                       lpSum([self.alpha[i] * self.tie_flow[i]] for i in range(len(self.tie_flow)))

    def solve_it(self):
        # self.problem += lpSum([self.gen_costs[i] * self.gen_vars[i] for i in range(len(self.gen_vars))]) - \
        #                 lpSum([self.alpha[i] * self.tie_flow[i]] for i in range(len(self.tie_flow)))
        self.problem.solve()
        for i in range(len(self.tie_flow)):
            print(self.tie_flow[i].value())
            print(self.alpha[i])

    def data_dump(self):
        # Data dump
        excel = pd.ExcelWriter('output_test.xlsx')
        gen_prods = []
        for i in range(len(self.gen_vars)):
            gen_prods.append(self.gen_vars[i].value())
        pd.DataFrame({'limit': self.gen_max, 'production': gen_prods},
                     columns=['limit', 'production']).to_excel(excel, sheet_name='gens')
        line_loads = []
        line_shadow = []
        line_flow_low = []
        line_flow_high = []
        for i in range(len(self.flow_vars)):
            line_loads.append(self.flow_vars[i].value())
            line_shadow.append(self.line_constraints[i].pi)
            line_flow_low.append(self.line_cap_constraint_low[i].pi)
            line_flow_high.append(self.line_cap_constraint_high[i].pi)
        pd.DataFrame({'limit': self.flow_lim, 'flow_loads': line_loads,
                      'susceptance_shadow': line_shadow,
                      'flow_low_shadow': line_flow_low,
                      'flow_high_shadow': line_flow_high},
                     columns=['limit', 'flow_loads', 'susceptance_shadow',
                              'flow_low_shadow', 'flow_high_shadow']).to_excel(excel, sheet_name='lines')
        lmp_list = []
        theta_vals = []
        for i in range(len(self.loads)):
            lmp_list.append(self.bus_constraints[i].pi)
            theta_vals.append(self.theta[i].value())
        pd.DataFrame({'bus_lmp': lmp_list, 'node_theta': theta_vals},
                     columns=['bus_lmp', 'node_theta']).to_excel(excel, sheet_name='bus')
        excel.close()

    def update_alpha(self, other_flow, iteration, A, B):
        for i in range(len(self.alpha)):
            print(str(self.tie_flow[i].value()) + ':' + str(other_flow[i]))
        print()
        for i in range(len(self.alpha)):
            k = 1/(A + iteration * B)
            s = self.tie_flow[i].value() + other_flow[i]
            if s != 0:
                self.alpha[i] += k * -s / abs(s)
