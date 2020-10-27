# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# October, 2020
# distributed_DCOPF_round3.py
# Third go at a distributed DC OPF.  Finally figured out how to implement Dr. Ranades method.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
import math


class node:
    def __init__(self, lines, load, a, b):
        self.lines = lines
        self.Pgen = 0  # Pgen is really Pinjected
        self.Pload = load
        self.a = a
        self.b = b
        self.ld = 0
        self.ld_sum = 0
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


class line:
    def __init__(self):
        self.Pnode = {}
        self.ld = 0.01
        self.balanced = False
        self.eps = .00001

    def update_lambda(self):
        total = np.sum([self.Pnode[x] for x in self.Pnode.keys()])
        # print(total)
        if total != 0:
            total_log = math.log(abs(total))
        else:
            total_log = 0
        if total < 0:
            if total_log > 1:
                self.ld += 1
            else:
                self.ld += .0001
        if total > 0:
            if total_log > 1:
                self.ld -= 1
            else:
                self.ld -= .0001
        # if abs(total) <= 0 + self.eps:
        #     self.balanced = True


if __name__ == '__main__':
    line_1 = line()
    line_2 = line()
    # line_3 = line()
    # node_1 = node([line_1, line_2], 0, 7.95, .001562)
    # node_2 = node([line_1, line_3], 0, 7.85, .00194)
    # node_3 = node([line_2, line_3], 300, None, None)

    node_1 = node([line_1], 0, 1, .0625)
    node_2 = node([line_1, line_2], 0, 1, .0125)
    node_3 = node([line_2], 100, None, None)
    i = 0
    while line_1.balanced is not True:
        i += 1
        node_1.update_ld()
        node_2.update_ld()
        node_3.update_ld()
        node_1.update_power()
        node_2.update_power()
        node_3.update_power()
        print('Node 1 power: ' + str(node_1.Pgen))
        print('Node 2 power: ' + str(node_2.Pgen))
        print('Node 3 power: ' + str(node_3.Pgen))
        print('Power transfers on line 1: ' + str(line_1.Pnode))
        print('Power transfers on line 2: ' + str(line_2.Pnode))
        print('Line 1 lambda: ' + str(line_1.ld))
        print('Line 2 lambda: ' + str(line_2.ld))
        line_1.update_lambda()
        line_2.update_lambda()
        # line_3.update_lambda()
        '''print(node_1.Pgen)
        print(node_2.Pgen)
        print(node_3.Pgen)
        print(line_1.ld)
        print(line_2.ld)
        print(line_3.ld)
        print()'''
        print()
        # if i == 200:
        #     exit()
    print(str(i) + ' iterations to completion')
