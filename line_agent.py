# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# August 2020
# line_agent.py
# Manage objects and communications for a line object.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from comm_manager_line import Line_comm
import threading

if __name__ == '__main__':
    # Allow both nodes to connect individually
    node_1 = Line_comm(b'5j')
    node_1.comm_connect(8080)
    node_2 = Line_comm(b'5j')
    node_2.comm_connect(8081)

    threading.Thread(target=node_1.communicate).start()
    threading.Thread(target=node_2.communicate).start()

    while True:
        node_1.other_v = node_2.v
        node_2.other_v = node_1.v
