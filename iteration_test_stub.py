# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# June 2020
# iteration_test_stub
# Test a possible iterative solution to settle power and Yself in Nodes.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import math

from gauss_node import Node
from line_agent import Line_Agent
from simulated_current_sensor import current_sensor

# Set up each line
l1_2 = Line_Agent(-46.15+30.77j)
l2_3 = Line_Agent(-4.615+3.077j)
l2_4 = Line_Agent(-4.615+3.077j)
ampBase = 100E6/138E3/math.sqrt(3)
c1_2 = current_sensor(465.78/ampBase)
c2_1 = current_sensor(465.78/ampBase)
c2_3 = current_sensor(232.71/ampBase)
c2_4 = current_sensor(233.08/ampBase)

# Create the Node objects with shared info object
Node1 = Node(1, 0, lines=[l1_2], slack=True, current_sensors=[c1_2])
Node2 = Node(1, 0, lines=[l1_2, l2_3, l2_4], current_sensors=[c2_1, c2_3, c2_4])

# Iterate over the live_pf function 1000 times, see if we get any changes?
for _ in range(1000):
    Node1.live_pf()
    Node2.live_pf()

print(Node1.selfY)
print(Node1.current_sensor_power)
print('\n')
print(Node2.selfY)
print(Node2.current_sensor_power)
