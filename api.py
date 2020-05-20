# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# January 2020
# api.py
# Run a REST style api to register RaspberryPis as distributed resources for the algorithm.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import flask
from flask import request
import time
import gevent.pywsgi as pywsgi
import hashlib

from admittance import Admittance
from gauss import Gauss

# Create a basic application through flask
app = flask.Flask(__name__)
# This will hold a list of active pys
pis = {}


# Basic page responds with info about the server in index.html.  Should eventually respond with a Readme
@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def home():
    return open('html/index.html', 'r').read()


# Search for a particular page in the html folder, return if exists.
@app.route('/<page>', methods=['GET', 'POST'])
def search_page(page):
    try:
        f = open('html/' + page, 'r').read()
        return f
    except FileNotFoundError:
        flask.abort(404)


# Register Raspberry Pi in the pys dictionary, return a timestamp.
@app.route('/register', methods=['POST'])
def register():
    pis[request.remote_addr] = {'timeStamp': time.localtime(), 'volts': request.args['volts'],
                                'power': request.args['power']}
    print(pis)
    return pis[request.remote_addr]


# Return information about the requester's neighbors
@app.route('/get_neighbor_volts_power', methods=['GET'])
def get_info():
    # For now, assume ALL Pis are neighbors
    neighbors = {}
    bad = []
    current_time = time.localtime()
    for neighbor in pis.keys():
        # First, ensure neighbors are < 15 minutes old, if they aren't remove them from the neighbor list
        if time.mktime(current_time) - time.mktime(pis[neighbor]['timeStamp']) <= 15 * 60 and \
                neighbor != request.remote_addr:
            neighbors[hashlib.sha512(neighbor.encode('utf-8')).hexdigest()] = {'volts': pis[neighbor]['volts'],
                                                                               'power': pis[neighbor]['power']}
        # If not itself, must be stale
        elif neighbor != request.remote_addr:
            bad.append(neighbor)

    # Remove stale Pis
    for old in bad:
        del (pis[old])

    # Return valid neighbors
    return neighbors


# Run the server with a wsgi host on whatever our IP is
server = pywsgi.WSGIServer(('10.0.0.10', 5000), app)
server.serve_forever()
