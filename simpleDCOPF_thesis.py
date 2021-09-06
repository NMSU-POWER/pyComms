# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# September 2021
# simpleDCOPF_thesis.py
# Example DCOPF and other algorithms used in thesis DCOPF chapter.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pulp import LpProblem, LpMinimize, LpVariable

gens = [LpVariable(name="g1", lowBound=0, upBound=150),
        LpVariable(name='g2', lowBound=0, upBound=150),
        LpVariable(name='g3', lowBound=0, upBound=150)]

costs = [1, 1.5, 2]

flows = [LpVariable('f1', lowBound=-200, upBound=200),
         LpVariable('f2', lowBound=-50, upBound=50),
         LpVariable('f3', lowBound=-150, upBound=150)]
