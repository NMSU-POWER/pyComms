# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# July 2020
# line_agent_v2.py
# REST api that runs on line agents.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import flask
from flask import request
import gevent.pywsgi as pywsgi

# Create a basic application through flask
app = flask.Flask(__name__)

# unverified, un-abstracted dictionary of the busses
bus = {}

# This value will be manually modified for now
myAdmittance = 1


# Push your voltage to the line agent
@app.route('/pushv', methods=['POST'])
def pushv():
    bus[request.remote_addr] = request.args['volts']


# Pull the other voltage value, 1 ifndef
@app.route('/pullv', methods=['GET'])
def pullv():
    for key in bus.keys():
        if key != request.remote_addr:
            return str(bus[key])
    return '1'


# Return the admittance of the line
@app.route('/pully', methods=['GET'])
def pully():
    return str(myAdmittance)


# Run the server with a wsgi host on whatever our IP is
server = pywsgi.WSGIServer(('10.0.0.234', 5000), app)
server.serve_forever()