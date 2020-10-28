# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# October, 2020
# distributed_DCOPF_round3.py
# Third go at a distributed DC OPF.  Finally figured out how to implement Dr. Ranades method.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
import math
from pulp import LpVariable, LpMinimize, LpProblem, lpSum


class node:
    def __init__(self, lines, load, a, b):
        self.lines = lines
        self.Pgen = 0  # Pgen is really Pinjected
        self.Pload = load
        self.a = a
        self.b = b
        self.ld = 0
        self.ld_sum = 0
        self.cost_per_mw = (1000 * a + 1000**2 * b)/1000
        for line in self.lines:
            line.Pnode[self] = 0

    def update_ld(self):
        self.ld = np.mean([x.ld for x in self.lines])
        self.ld_sum = np.sum([x.ld for x in self.lines])

    # Problem in update_power, specifically with the export calc
    def update_power(self):
        self.Pgen = 0
        # This is where the error is, let's to pseudo-code to find it
        # For every line connected to this node
        #  The export value starts as the generation at the node, minus the load at the node
        #  For every line connected to the node except the current line
        #   subtract the export to the other lines
        for line in self.lines:
            if self.a is not None or self.b is not None:
                gen_for_line = (line.ld - self.a) / (2 * self.b)
                self.Pgen += gen_for_line
                # self.Pgen = (self.ld - self.a) / (2 * self.b)
            else:
                gen_for_line = 0
            export = gen_for_line - self.Pload
            # export = self.Pgen - self.Pload
            for other_lines in self.lines:
                export -= other_lines.Pnode[self]
            export += line.Pnode[self]
            line.Pnode[self] = gen_for_line - self.Pload

    def minimize(self):
        model = LpProblem(name='nodal_minimize', sense=LpMinimize)
        powerVar = LpVariable('Nodal_power', lowBound=0, upBound=1000)
        line_vars = {}
        for line in self.lines:
            line_vars[LpVariable('line_' + str(line), lowBound=line.limits[0],
                                 upBound=line.limits[1])] = (line.ld, line)
        # We have all the variables, compile them
        model += self.cost_per_mw * powerVar - lpSum([key * line_vars[key][0] for key in line_vars.keys()])
        model += -1 * powerVar + lpSum([key for key in line_vars.keys()]) == -1 * self.Pload
        model.solve()
        print(powerVar.value())
        self.Pgen = powerVar.value()
        for key in line_vars.keys():
            print(key.value())
            line_vars[key][1].Pnode[self] = key.value()
        print()


class line:
    def __init__(self, lower, upper):
        self.Pnode = {}
        self.ld = 0
        self.balanced = False
        self.eps = .00001
        self.limits = (lower, upper)

    def update_lambda(self):
        total = np.sum([self.Pnode[x] for x in self.Pnode.keys()])
        # print(total)
        if total != 0:
            total_log = math.log(abs(total))
        else:
            total_log = 0
        if total < 0:
            # if total_log > 1:
            #     self.ld += 1
            # else:
            self.ld += .01
        if total > 0:
            # if total_log > 1:
            #     self.ld -= 1
            # else:
            self.ld -= .01
        # if abs(total) <= 0 + self.eps:
        #     self.balanced = True


if __name__ == '__main__':
    line_1 = line(-1000, 1000)
    node_1 = node([line_1], 0, 1, .0625)
    node_2 = node([line_1], 960, 1, .0125)
    # node_3 = node([line_2], 100, None, None)
    i = 0
    while line_1.balanced is not True:
        i += 1
        node_1.minimize()
        node_2.minimize()
        line_1.update_lambda()
        print(node_1.Pgen)
        print(node_2.Pgen)
        print(line_1.Pnode)
        print(line_1.ld)
        # if i == 200:
        #     break
        print()
    print(str(i) + ' iterations to completion')
