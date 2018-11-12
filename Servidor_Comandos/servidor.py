from flask import Flask, request
from comandos import ComandosResidencia
import json

app = Flask(__name__)
residencia = ''
# https://stackoverflow.com/questions/15486570/bluetooth-communication-between-arduino-and-pybluez

@app.route('/', methods=['GET'])
def comando_residencia():
    RPC = json.dumps(request.form['RPC'])
    residencia.executa(RPC['method'], RPC['args'])

    return ''


@app.route('/<method>/<int:status>', methods=['GET'])
def teste(method, status):
    status = bool(status)

    residencia.executa(method, status)
    return json.dumps({method: status})


if __name__ == '__main__':
    residencia = ComandosResidencia(bt_addr="00:12:10:23:10:18")
    app.run(debug=True, port=5000)
