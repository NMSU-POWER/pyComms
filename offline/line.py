# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March 2021
# line.py
# Perform operations that pertain to being a line object.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from statistics import mean

class Line:
    def __init__(self, y, id_input=-1):
        self.y = y
        self.x = (1 / self.y).imag
        self.device_id = id_input
        self.ld = 0
        self.alpha = -.001
        self.delta = {}
        self.ptie = {}
        print("line " + str(self.device_id) + " setup.")

    def update_lambda(self, other_ld):
        self.ld = self.ld + self.alpha * sum([self.ptie[x] for x in self.ptie.keys()])
        other_ld.append(self.ld)
        self.ld = mean(other_ld)
