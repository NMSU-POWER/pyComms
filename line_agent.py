# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# August 2020
# line_agent.py
# Manage objects and communications for a line object.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from comm_manager_line import Line_comm
import threading

if __name__ == '__main__':
    # Create and connect to the first node
    node_1 = Line_comm(b'-.44+6.64j')
    node_1.comm_connect(8080)
    # Create and connect to the second node
    node_2 = Line_comm(b'-.44+6.64j')
    node_2.comm_connect(8081)

    # Node threads need to be started to create a constant spinning communication to both nodes
    threading.Thread(target=node_1.communicate).start()
    threading.Thread(target=node_2.communicate).start()

    while True:
        # Node 1 needs to have node 2's voltage
        node_1.other_v = node_2.v
        # Node 2 needs to have node 1's voltage
        node_2.other_v = node_1.v
