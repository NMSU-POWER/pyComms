# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# January 2020
# client.py
# Perform checks continually? to see changes to volts and power and update own
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import requests
import random
import time

myVolts = 120 - random.randint(0, 1)
myPower = random.randint(100, 1000)

print(myVolts, myPower)

while(1):
    response = requests.post('http://172.24.61.209:5000/register', params={'volts': myVolts, 'power': myPower})
    response = requests.get('http://172.24.61.209:5000/get_neighbor_volts_power')
    piList = response.content
    print(piList)
    time.sleep(30)
