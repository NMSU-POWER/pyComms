import flask
import time
import gevent.pywsgi as pywsgi

app = flask.Flask(__name__)
pys = {}


@app.route('/', methods=['GET'])
def home():
    return '<h1>Py server alpha version</h1>'


@app.route('/register', methods=['POST', 'GET'])
def register():
    pys[flask.request.remote_addr] = time.localtime()
    print(pys)
    return {'update_time': pys[flask.request.remote_addr]}


server = pywsgi.WSGIServer(('10.0.0.2', 5000), app)
server.serve_forever()
