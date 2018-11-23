from simplecrypt import encrypt
import requests, json

password = 'SOD2018'

def led(id=0, status=0):
    _executa('led', [id, status])

def alarme(status=0):
    _executa('alarme', [status])

def temperatura(status=0):
    _executa('temperatura', [status])

def _executa(method, params):
    data_cript = _criptografar({
                    'method': method,
                    'params': params
                })

    requests.post('http://192.168.1.125:5001', data=data_cript)

def _criptografar(data):
    data = json.dumps(data)
    return encrypt(password, data)
