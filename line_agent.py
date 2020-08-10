# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# August 2020
# line_agent.py
# Manage objects and communications for a line object.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from comm_manager_line import Line_comm
import threading

if __name__ == '__main__':
    # Create the first node link
    node_1 = Line_comm(y=b'-.44+6.64j', port=8080)
    # Create the second node link
    node_2 = Line_comm(y=b'-.44+6.64j', port=8081)

    # Node threads need to be started to create a constant spinning communication to both nodes
    threading.Thread(target=node_1.communicate).start()
    threading.Thread(target=node_2.communicate).start()

    while True:
        # Node 1 needs to have node 2's voltage
        node_1.other_v = node_2.v
        # Node 2 needs to have node 1's voltage
        node_2.other_v = node_1.v
