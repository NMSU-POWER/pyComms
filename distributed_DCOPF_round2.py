# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# October, 2020
# distributed_DCOPF_round2.py
# Second go at a distributed DC OPF.  Starting from scratch given the number of changes from go 1.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from statistics import mean

# Using previous iterations as templates, the line should be very simple.
class line:
    def __init__(self, admittance):
        self.angle = {}  # Each bus needs to provide and update its angle
        self.ld = 0
        self.price = {}
        self.admittance = admittance


class node:
    def __init__(self, lines,  a, b, load=0, slack=False):
        self.lines = lines
        self.a = a
        self.b = b
        self.load = load
        self.slack = slack
        self.angle = 0
        self.ld = 0
        self.gen = 0
        self.angles = {}

    # This is where it gets complicated and fuzzy.  Who decides what the lambda is?  Lambda decides how much we produce.
    #  This is because we want to compare our cost with the cost of buying from the other line.  This means we need to
    #  figure out what lambda should be, based on the lambda of the other node?  Can we straight compare, find the
    #  minimum price between purchase x at this rate and produce y at this rate?
    # How does our own lambda factor into the calculation?  It's our profit for export.  There's no way around it,
    #  the lambdas across a line MUST be equal because one node can't charge more for power than the other node is paying.
    # Ignoring this for now, can we develop an algorithm where they will come to this result without knowing they're equal?
    def gen_calc(self):
        # Step 1: find out how much the angles say we export.
        export = self.export_calc()
        # Step 2: Price this export with our lambda
        price = self.ld * export
        # Step 2.5: Check our price of export with the lines price of export?  Line lambda up if price to produce > export
        #  This is because we have to agree on a price between the two, this goes back to shared lambda
        #  Essentially, ball goes to load buses, they need to say: okay fine increase lambda and i'll still buy some
        for line in self.lines:
            for bus in line.angle.keys():
                if bus != self:
                    if line.ld < self.a + 2 * self.b * self.quick_export(line.angle[bus], line.admittance):
                        line.ld += .001
                    else:
                        line.ld -= .001
        # Step 3: Adjust the lambda upward if the price of export is < price to produce that much
        #  We want lambda to be the AVERAGE of the total value to export on all lines.
        #  ^ The line lambda and the bus lambda ARE DIFFERENT LAMBDAS.  For now, let's make line lambda = average of both?
        #  Later, it should be different, but I'm not sure what.
        self.ld = mean([x for x in self.lines.ld])
        # Step 4: Calculate desired generation at rates
        for line in self.lines:
            self.gen += self.a / (line.ld - 2 * self.b)
        # Step 5 if not slack: Adjust our angle to reflect the desired net export from each line
        # Keep track of all connected lines, log the angle across?  We can find the difference between each bus and all
        #  the others? will that help?
        # For each angle:
        if self.slack == False:
            for line in self.lines:
                self.angles[line] =


    # Single line export value
    def quick_export(self, angle, admittance):
        return 100 * angle * admittance

    # Pretty straightforward, given the angles, how much power are we shipping out.
    def export_calc(self):
        export = 0
        other_angle = self.angle
        for line in self.lines:
            admittance = line.admittance
            for key in line.angle.keys():
                if key != self:
                    other_angle = line.angle[key]
            export += other_angle * admittance * 100

