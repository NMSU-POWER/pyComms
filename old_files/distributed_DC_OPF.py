# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# September 2020
# distributed_DC_OPF
# Run a basic DC OPF as a distributed system.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import threading

class bus:
    def __init__(self, pLoad, export, a, b, pGen=0, id=0,  slack=False):
        # straightforward: this component should change as the algorithm progresses
        self.gen = pGen
        # This is obvious, if there's a load it goes here
        self.load = pLoad
        # This will be gen - load, do we need it?  Yes. This must be how we ship out power?
        self.export = export
        # These are generator cost constants
        self.a = a
        self.b = b
        self.lambda_line = {}
        self.delta = 0
        self.slack = slack
        self.id = id

    def power_calc(self, del_other, ld, line):
        self.lambda_line[line] = ld
        self.gen = (self.lambda_line[line] - self.a) / (2 * self.b)
        self.export = 0
        for lines in self.lambda_line:
            if lines != line:
                self.export += (self.lambda_line[lines] - self.a) / (2 * self.b)
        if not self.slack:
            self.delta = (self.gen - self.load - self.export) / 1000 + del_other
        print(str(self.id) + ': ' + str(self.gen))
        return self.gen - self.load


class line:
    def __init__(self, bus1, bus2):
        self.bus1 = bus1
        self.bus2 = bus2
        self.ld_line = 0

    def run(self):
        difference = self.bus1.power_calc(self.bus2.delta, self.ld_line, self) + \
                     self.bus2.power_calc(self.bus1.delta, self.ld_line, self)
        epsilon = .001
        while difference < 0 - epsilon or difference > 0 + epsilon:
            if difference < 0:
                self.ld_line += .001
            else:
                self.ld_line -= .001
            difference = self.bus1.power_calc(self.bus2.delta, self.ld_line, self) + \
                         self.bus2.power_calc(self.bus1.delta, self.ld_line, self)


# Essentially a line
if __name__ == "__main__":
    ld_line = 0
    bus1 = bus(0, 0, 7.92, .001562 * 2, 0, 1, True)
    bus2 = bus(0, 0, 7.85, .00194 * 2, 0, 2, False)
    bus3 = bus(300, 0, 7.97, float('inf'), 0, 3, False)

    # Duh. These need to be parallel, we're getting stuck in #1
    line1 = line(bus1, bus2)
    threading.Thread(target=line1.run).start()
    line2 = line(bus2, bus3)
    threading.Thread(target=line2.run).start()
    line3 = line(bus1, bus3)
    threading.Thread(target=line3.run).start()

    print(line1.bus1.gen)
