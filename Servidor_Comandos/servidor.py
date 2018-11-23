from flask import Flask, request
from Crypto.Cipher import AES
from comandos import HomeControl
import json

password = 'SOD-2018SOD-2018'
cripto = AES.new(password)

home_control = None
app = Flask(__name__)


@app.route('/', methods=['POST'])
def comando_home_control():
    start_home_control()
    
    data_cript = request.data
    data = cripto.decrypt(data_cript)

    # Remove os caracteres adicionados
    data_str = data.decode()
    data_str = data_str.rpartition('#')[0]

    data = json.loads(data_str)
    print('RPC Data: ', data)

    home_control.executa(data['method'], data['params'])
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
    app.run(debug=True, host='192.168.1.125', port=5001)
