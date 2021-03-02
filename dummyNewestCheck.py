# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# February 2021
# dummyNewestCheck.py
# Proof of functionality without moving to the cluster.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import time
import json

# We need to simulate the objects used below as closely as needed without spending too much time.
# First, the internal object, since it's easier
bucket_dict = {'1': [time.time(), 'line', 5, 10],
               '2': [time.time()+50, 'line', 10, 15]}
# Now the objects from the lines.  This will be a dictionary inside another dictionary, all brought to binary then back.
recval1 = str({'buckets': {'3': [time.time(), 'node', 0,  5],
                           '4': [time.time()-50, 'node', 10, 15]}}).encode()

recval2 = str({'buckets': {'5': [time.time()-150, 'node', 100, 105],
                           '6': [time.time()-100, 'node', 150, 155],
                           '2': [time.time()+100, 'line', 100, 105]}}).encode()


recval1 = json.loads(recval1.decode().replace("'", '"'))
recval2 = json.loads(recval2.decode().replace("'", '"'))

# Before starting, all dictionaries, self first
print(bucket_dict)
print(recval1)
print(recval2)

# First we need to know how many unique dictionary keys there are.
unique = []
unique.extend(bucket_dict.keys())
unique.extend(recval1['buckets'].keys())
unique.extend(recval2['buckets'].keys())
unique = set(unique)
for key in unique:
    # Assuming this worked and we now have a set of unique keys
    # First step, see where the key exists, pull the values from these locations
    compare = []
    if key in bucket_dict.keys():
        compare.append(bucket_dict[key])
    if key in recval1['buckets'].keys():
        compare.append(recval1['buckets'][key])
    if key in recval2['buckets'].keys():
        compare.append(recval2['buckets'][key])
    # If all went well, we have at least one value in compare, and up to 3 values
    # Find the newest of these values
    times = [x[0] for x in compare]
    index = times.index(max(times))
    newest = compare[index]
    # Theoretically, newest should contain the newest instance of the data
    bucket_dict[key] = newest
    # IFF everything goes right, we now hold the value we want.  Need to do some small testing to confirm.

print(bucket_dict)