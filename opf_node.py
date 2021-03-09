# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# January 2021
# opf_node.py
# Be a node and run individual DCOPF functions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import statistics
import threading
import sys
import json
import time
import node_verify
from comm_node import NodeConnection


# Hold information about the line in a simple object
class Line:
    def __init__(self, comm_chanel, id):
        self.local_delta = 0
        self.power_out = 0
        self.line_reactance = 0
        self.other_delta = 0
        self.comm_object = comm_chanel
        self.line_lambda = 0
        self.other_lambdas = []
        self.id = id
        self.bucket_dict = {str(self.id): [time.time(), 'node', 0, 5, 'Unsolved']}
        self.comm_object.provided_value = str({"delta": self.local_delta,
                                               "other_lambdas": self.other_lambdas,
                                               "power_out": self.power_out,
                                               "buckets": self.bucket_dict}).encode()

    def gather_info(self):
        try:
            recd = json.loads(self.comm_object.received_value.decode().replace("'", '"'))
        except Exception as e:
            print(e)
            return
        self.line_reactance = recd['reactance']
        self.other_delta = recd['other_delta']
        self.line_lambda = recd['lambda']
        # Need to process incoming values here
        # This is stage one, where the internal line objects pick new values that come in vs what we have.
        # This is simpler than the line case, since we only every have two values to look at, our own + the remote one
        incoming_bucket = recd['buckets']
        # We can break the pattern from the lines based on this simplicity.  We simply need to check our local
        # dictionary for each of the keys in the incoming dictionary.  Iff we have a copy, we can compare time stamps.
        # If we don't have a copy, simply import this new value.
        for key in incoming_bucket.keys():
            if key in self.bucket_dict.keys():
                if self.bucket_dict[key][0] < incoming_bucket[key][0]:
                    self.bucket_dict[key] = incoming_bucket[key]
            else:
                # Must not exist locally
                self.bucket_dict[key] = incoming_bucket[key]
        # That should actually do it for here.
        self.comm_object.provided_value = str({"delta": self.local_delta,
                                               "other_lambdas": self.other_lambdas,
                                               "power_out": self.power_out,
                                               "buckets": self.bucket_dict}).encode()


# Hold information pertaining to the specific bus (node)
class Node:
    def __init__(self, load, a, b, lines, id, slack=False):
        # Initialization angle is always 0
        self.delta = 0
        # load is assigned at start (for now)
        self.load = load
        # Power initializes to 0
        self.power = 0
        # Trailing constant on power cost
        self.a = a
        # Linear component of power cost
        self.b = b
        # Unique ID (provided at startup for now)
        self.id = id
        # list of internalLine objects (or ips)
        self.lines = lines
        # reactance summation
        self.reactanceSum = sum([1 / x.line_reactance for x in self.lines])
        # set up our delta in the lines
        for line in self.lines:
            line.local_delta = self.delta
            line.power_out = 0
        # Value to distribute
        self.bucket_dict = {str(self.id): [time.time(), 'node', 0, 5, 'Unsolved']}
        # self.send_out = str({"id": self.id}).encode()

    # All the node's calculations can happen in one shot
    def update_power_angle(self):
        # Update power first
        self.power = (statistics.mean([x.line_lambda for x in self.lines]) - self.a) / 2 / self.b
        self.bucket_dict[str(self.id)] = [time.time(), 'node', int(self.power/10)*10, int(self.power/10)*10+10]
        # Now update self angle
        delta_reactance = []
        for line in self.lines:
            delta_reactance.append((line.other_delta, line.line_reactance))
        self.delta = (self.power - self.load + sum([x[0] / x[1] for x in delta_reactance])) / self.reactanceSum
        for line in self.lines:
            line.local_delta = self.delta
        # We should update the buckets here.  At this point, the node can run comparisons for the whole system
        # and inject new values into itself then copy into the lines.
        # This will happen one step BEFORE the lines update any values.
        unique = []
        unique.extend(self.bucket_dict.keys())
        for line in self.lines:
            unique.extend(line.bucket_dict.keys())
        unique = set(unique)
        # We should have all unique keys.
        for key in unique:
            # Assuming this worked and we now have a set of unique keys
            # First step, see where the key exists, pull the values from these locations
            compare = []
            if key in self.bucket_dict.keys():
                compare.append(self.bucket_dict[key])
            for line in self.lines:
                if key in line.bucket_dict.keys():
                    compare.append(line.bucket_dict[key])
            '''if key in recval1['buckets'].keys():
                compare.append(recval1['buckets'][key])
            if key in recval2['buckets'].keys():
                compare.append(recval2['buckets'][key])'''
            # If all went well, we have at least one value in compare, and up to 3 values
            # Find the newest of these values
            times = [x[0] for x in compare]
            index = times.index(max(times))
            newest = compare[index]
            # Theoretically, newest should contain the newest instance of the data
            self.bucket_dict[key] = newest
            # IFF everything goes right, we now hold the value we want.  Need to do some small testing to confirm.
        # Now update the power transferred out on this side of the line object
        for line in self.lines:
            # Distribute the buckets
            line.bucket_dict = self.bucket_dict
            line.power_out = (self.delta - line.other_delta) / line.line_reactance
            lambdas = []
            for line_for_lambda in self.lines:
                if line_for_lambda != line:
                    lambdas.append(line_for_lambda.line_lambda)
            line.other_lambdas = lambdas


if __name__ == '__main__':
    comms = []
    threads = []
    print('Initializing connection objects...')
    for line_ip in sys.argv[5:]:
        comm = NodeConnection(ip=line_ip, provvalue=b'initialize', port=8080)
        comms.append(comm)
        threads.append(threading.Thread(target=comm.trade_values, daemon=True).start())
    lines = []
    print('Initializing line objects...')
    for comm in comms:
        lines.append(Line(comm, id=int(sys.argv[4])))
    print('Waiting for line connections...')
    for line in lines:
        while line.comm_object.connected is False:
            continue
        line.gather_info()
    print('Initializing node...')
    node = Node(load=float(sys.argv[1]), a=float(sys.argv[2]), b=float(sys.argv[3]), id=int(sys.argv[4]), lines=lines)
    # Time to actually run stuff
    while True:
        # Add in logic here to decide if we run again
        node.update_power_angle()
        # print(node.power)
        for line in lines:
            line.gather_info()
        print('Node')
        print(node.bucket_dict)
        solved = node_verify.check_validity(node.bucket_dict)
        node.bucket_dict[str(node.id)][3] = solved
        print(solved)
        time.sleep(2)
