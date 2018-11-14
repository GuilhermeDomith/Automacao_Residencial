from flask import Flask, request
from comandos import HomeControl
import json

home_control = None
app = Flask(__name__)

@app.route('/', methods=['GET'])
def comando_home_control():
    global home_control
    '''RPC = json.dumps(request.form['RPC'])

    if not home_control:
        home_control = HomeControl(bt_addr="20:16:10:25:34:24")

    home_control.executa(RPC['method'], RPC['args'])
    return '''


@app.route('/<method>/<int:status>', methods=['GET'])
def teste(method, status):
    status = bool(status)

    home_control.executa(method, status)
    return json.dumps({method: status})

def start_home_control():
    global home_control

    if not home_control:
        home_control = HomeControl(bt_addr="20:16:10:25:34:24")

if __name__ == '__main__':
    start_home_control()
    app.run(debug=True, port=5000)