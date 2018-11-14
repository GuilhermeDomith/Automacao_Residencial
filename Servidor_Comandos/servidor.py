from flask import Flask, request
from comandos import HomeControl
import json

home_control = None
app = Flask(__name__)

@app.route('/', methods=['GET'])
def comando_home_control():
    #RPC = json.dumps(request.form['RPC']
    start_home_control()

    #home_control.executa(RPC['method'], RPC['args'])
    return json.dumps({'status': 'ok'})


@app.route('/<method>/<status>', methods=['GET'])
def teste(method, status):

    home_control.executa(method, status)
    return json.dumps({method: status})

def start_home_control():
    global home_control

    if not home_control:
        home_control = HomeControl(bt_addr="20:16:10:25:34:24")

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.126', port=5000)