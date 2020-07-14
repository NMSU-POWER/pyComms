# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# June 2020
# parallel_distributed_gauss.py
# Observe the power flow as it's executed by nodes.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from gauss_node import Node
from gauss_node_bad import Node as badNode
from line_agent import Line_Agent
import threading

# Set up each line
l1_2 = Line_Agent(-46.15+30.77j)
l2_3 = Line_Agent(-4.615+3.077j)
l2_4 = Line_Agent(-4.615+3.077j)

# Create the Node objects with shared info object
Node1 = Node(1, 0, [l1_2], slack=True)
Node2 = Node(.9826, 0, [l1_2, l2_3, l2_4])
Node3 = badNode(1, -.50, [l2_3])
Node4 = Node(.8975, -.50, [l2_4])

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

try:
    while True:
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
        print('Problems: ')
        print(Node1.problem)
        print(Node2.problem)
        print(Node3.problem)
        print(Node4.problem)
        print('\n')
except:
    # exception out of gauss loop, close threads
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
