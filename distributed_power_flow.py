# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# May 2020
# distributed_power_flow.py
# Observe the power flow as it's executed.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from gauss_node import Node
import math

Node1 = Node(1, 1.112+.074j, [.9826], [-46.15+30.77j])
Node2 = Node(.9826, 0, [1, .8975, .8975], [-45.15+30.77j, -45.15+30.77j, -45.15+30.77j])
Node3 = Node(.8975, -50, [.9826], [-45.15+30.77j])
Node4 = Node(.8975, -50, [.9826], [-45.15+30.77j])

# Calculate the next bus angle from bus 1
delta = Node1.angle_calculation()
# Set bus 1 angle to known
Node1.neighborDelta = [math.radians(delta)]
# Set bus 2 to know its own angle
Node2.selfV = .9826 * (math.cos(math.radians(delta)) + 1j * math.sin(math.radians(delta)))
