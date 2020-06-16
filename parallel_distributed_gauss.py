# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# June 2020
# parallel_distributed_gauss.py
# Observe the power flow as it's executed by nodes.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from gauss_node import Node
from gauss_node import shared_info
import threading

# Set up the shared information for each node
Node1_share = shared_info(neighborV=[1], neighborY=[-46.15+30.77j], slack=True)
Node2_share = shared_info(neighborV=[1, 1, 1], neighborY=[-46.15+30.77j, -4.615+3.077j, -4.615+3.077j])
Node3_share = shared_info(neighborV=[1], neighborY=[-4.615+3.077j])
Node4_share = shared_info(neighborV=[1], neighborY=[-4.615+3.077j])

# Create the Node objects with shared info object
Node1 = Node(1, 0, Node1_share)
Node2 = Node(1, 0, Node2_share)
Node3 = Node(1, -.50, Node3_share)
Node4 = Node(1, -.50, Node4_share)

# Assign each Node a thread
thread1 = threading.Thread(target=Node1.node_manager)
thread2 = threading.Thread(target=Node2.node_manager)
thread3 = threading.Thread(target=Node3.node_manager)
thread4 = threading.Thread(target=Node4.node_manager)

# Start up the threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()

i = 0

try:
    while True:
        # V1 info
        Node1_share.neighborV = [Node2.selfV]

        # V2 info
        Node2_share.neighborV = [Node1.selfV, Node3.selfV, Node4.selfV]

        # V3 info
        Node3_share.neighborV = [Node2.selfV]

        # V4 info
        Node4_share.neighborV = [Node2.selfV]

        # Print information for user
        print('Voltages:')
        print(Node1.selfV)
        print(Node2.selfV)
        print(Node3.selfV)
        print(Node4.selfV)
        print('Powers:')
        print(Node1.selfS)
        print(Node2.selfS)
        print(Node3.selfS)
        print(Node4.selfS)
        print('\n')

        i += 1
        if i == 20:
            Node3.selfS = -1
except:
    # exception out of gauss loop, close threads
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
