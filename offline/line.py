# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March 2021
# line.py
# Perform operations that pertain to being a line object.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from statistics import mean

class Line:
    def __init__(self, y, conn1, conn2, limit=0, id_input=-1):
        self.y = y
        self.x = (1 / self.y).imag
        self.conn1 = conn1
        self.conn2 = conn2
        self.device_id = id_input
        self.ld = 0
        self.alpha = -.001
        self.beta = -.001
        self.delta = {}
        self.ptie = {}
        self.flow = {}
        self.limit = limit

    def update_lambda(self, other_ld):
        self.ld = self.ld + self.alpha * sum([self.ptie[x] for x in self.ptie.keys()])
        other_ld.append(self.ld)
        self.ld = mean(other_ld)

    def update_flow(self):
        if self.limit <= 0:
            return
        for key in self.ptie.keys():
            if self.ptie[key] > 0:
                self.flow[key] = self.flow[key] + self.beta * (self.ptie[key] - self.limit)
            else:
                self.flow[key] = self.flow[key] + self.beta * (self.ptie[key] + self.limit)
