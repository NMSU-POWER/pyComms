# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# May 2020
# distributed_power_flow.py
# Observe the power flow as it's executed.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from gauss_node import Node
import math
import numpy as np

Node1 = Node(1, 0, [.9826], [-46.15+30.77j])
Node2 = Node(.9826, 0, [1, 1, 1], [-46.15+30.77j, -4.615+3.077j, -4.615+3.077j])
Node3 = Node(1, -.50, [.9826], [-4.615+3.077j])
Node4 = Node(1, -.50, [.9826], [-4.615+3.077j])

# Calculate the next bus angle from bus 1
# delta = Node1.angle_calculation()
# Set bus 1 angle to known
# Node1.neighborDelta = [math.radians(delta)]
# Set bus 2 to know its own angle
# Node2.selfV = .9826 * (math.cos(math.radians(delta)) + 1j * math.sin(math.radians(delta)))

# Run a normal set of Gauss iterations, only change is that node calculations are inside the Node class.
for i in range(200):
    # Run voltage calculation on each bus
    v1, del1 = Node1.gauss_voltage()
    v2, del2 = Node2.gauss_voltage()
    v3, del3 = Node3.gauss_voltage()
    v4, del4 = Node4.gauss_voltage()

    # Set node 1 neighbors
    Node1.selfV = v1 * (math.cos(del1) + 1j * math.sin(del1))
    Node1.neighborDelta = [del2]
    Node1.neighborV = [v2]

    # Set node 2 voltage + neighbors
    Node2.selfV = v2 * (math.cos(del2) + 1j * math.sin(del2))
    Node2.neighborDelta = [del1, del3, del4]
    Node2.neighborV = [v1, v3, v4]

    # Set node 3 voltage + neighbors
    Node3.selfV = v3 * (math.cos(del3) + 1j * math.sin(del3))
    Node3.neighborDelta = [del2]
    Node3.neighborV = [v2]

    # Set node 4 voltage  neighbors
    Node4.selfV = v4 * (math.cos(del4) + 1j * math.sin(del4))
    Node4.neighborDelta = [del2]
    Node4.neighborV = [v2]

    # Get new S for node 1
    Node1.power_calc()

    # Reset Node1
    Node1.selfV = 1
    Node2.neighborDelta = [0, del3, del4]
    Node2.neighborV = [1, v3, v4]

print(Node1.selfV)
print(Node2.selfV)
print(Node3.selfV)
print(Node4.selfV)
