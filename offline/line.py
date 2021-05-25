# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March 2021
# line.py
# Perform operations that pertain to being a line object.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from statistics import mean

class Line:
    def __init__(self, y, conn1, conn2, id_input=-1):
        self.y = y
        self.x = (1 / self.y).imag
        self.conn1 = conn1
        self.conn2 = conn2
        self.device_id = id_input
        self.ld = 0
        self.alpha = -.001
        self.delta = {}
        self.ptie = {}

    def update_lambda(self, other_ld):
        self.ld = self.ld + self.alpha * sum([self.ptie[x] for x in self.ptie.keys()])
        other_ld.append(self.ld)
        self.ld = mean(other_ld)
