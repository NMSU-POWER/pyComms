# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# May 2020
# distributed_power_flow.py
# Observe the power flow as it's executed.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from gauss_node import Node
import math

Node1 = Node(1, 1.112+.074j, [.9826], [-46.15+30.77j])
Node2 = Node(.9826, 0, [1, .8975, .8975], [-46.15+30.77j, -46.15+30.77j, -46.15+30.77j])
Node3 = Node(.8975, -50, [.9826], [-46.15+30.77j])
Node4 = Node(.8975, -50, [.9826], [-46.15+30.77j])

# Calculate the next bus angle from bus 1
delta = Node1.angle_calculation()
# Set bus 1 angle to known
# Node1.neighborDelta = [math.radians(delta)]
# Set bus 2 to know its own angle
# Node2.selfV = .9826 * (math.cos(math.radians(delta)) + 1j * math.sin(math.radians(delta)))
for i in range(100):
    # Done !! This sets the self, but isn't broadcasting to neighbors, need to broadcast to neighbors
    Node1.gauss_voltage() # Problem might be here?: does v1 need to change before it goes back to 1?
    v2, del2 = Node2.gauss_voltage()
    Node1.neighborDelta = [del2]
    Node1.neighborV = [v2]
    Node2.selfV = v2 * (math.cos(del2) + 1j * math.sin(del2))
    v3, del3 = Node3.gauss_voltage()
    Node3.selfV = v3 * (math.cos(del3) + 1j * math.sin(del3))
    v4, del4 = Node4.gauss_voltage()
    Node2.neighborDelta = [0, del3, del4]
    Node2.neighborV = [1, v3, v4]
    Node4.selfV = v4 * (math.cos(del4) + 1j * math.sin(del4))
    Node3.neighborDelta = [del2]
    Node3.neighborV = [v2]
    Node4.neighborDelta = [del2]
    Node4.neighborV = [v2]

print(Node1.selfV)
print(Node2.selfV)
print(Node3.selfV)
print(Node4.selfV)
