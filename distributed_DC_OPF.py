# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# September 2020
# distributed_DC_OPF
# Run a basic DC OPF as a distributed system.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Going to start with the 2 bus case Dr. Ranade presented, some significant looking kinks with more busses.
# This is not OPF, this is ED
# There is no consideration of losses in the line, no consideration of the line having impedance.

class bus:
    def __init__(self, pLoad, export, a, b, pGen = 0):
        # straightforward: this component should change as the algorithm progresses
        self.gen = pGen
        # This is obvious, if theres a load it goes here
        self.load = pLoad
        # This will be gen - load, do we need it?
        self.export = export
        # These are generator cost constants
        self.a = a
        self.b = b
        self.lambda_line = 0
        self.delta = 0

    def power_calc(self, del_other, ld):
        self.lambda_line = ld
        self.gen = (self.lambda_line - self.a) / (2 * self.b)
        self.delta = (self.gen - self.load) / 1000 + del_other
        return self.gen - self.load


# Essentially a line
if __name__ == "__main__":
    ld_line = 0
    bus1 = bus(0, 0, 1, .0625, 0)
    bus2 = bus(960, 0, 1, .0125, 0)
    difference = bus1.power_calc(bus2.delta, ld_line) + bus2.power_calc(bus1.delta, ld_line)
    epsilon = .001
    while difference < 0 - epsilon or difference > 0 + epsilon:
        if difference < 0:
            ld_line += .001
        else:
            ld_line -= .001
        print(difference)
        print(ld_line)
        print(bus1.gen)
        print(bus2.gen)
        print()
        difference = bus1.power_calc(bus2.delta, ld_line) + bus2.power_calc(bus1.delta, ld_line)
    print(difference)
    print(ld_line)
    print(bus1.gen)
    print(bus2.gen)
