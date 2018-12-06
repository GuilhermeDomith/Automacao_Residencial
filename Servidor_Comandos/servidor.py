from flask import Flask, request
from Crypto.Cipher import AES
from comandos import HomeControl
from base64 import b64decode
import json, config

passwd_criptografia = 'sistemasdistribuidos2018'

home_control = None
app = Flask(__name__)


def descriptografar(data):
    #print('data dict ', data, type(data))    

    data_cript = b64decode(data['data'].encode())
    nonce = b64decode(data['nonce'].encode())
    
    #print('data cript', data_cript, type(data_cript))
    #print('nonce', nonce, type(nonce))

    cripto = AES.new(passwd_criptografia.encode(), AES.MODE_EAX, nonce=nonce)
    data = cripto.decrypt(data_cript)
    #print('data ', data, type(data))

    return data


@app.route('/', methods=['POST'])
def comando_home_control():
    start_home_control()

    #print(request.form)
    data_str = descriptografar(request.form)
    data = json.loads(data_str)
    #print('RPC Data: ', data)

    jsonResponse = home_control.executa(data['method'], data['params'])
    #print(jsonResponse)
    return jsonResponse

def start_home_control():
    global home_control

    if not home_control:
        home_control = HomeControl(bt_addr= config.bluetooth_addr)

if __name__ == '__main__':
    app.run(debug=True, host=config.servidor_rpc, port=config.porta_srpc)

