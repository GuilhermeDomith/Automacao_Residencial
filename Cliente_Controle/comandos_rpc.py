from simplecrypt import encrypt
import requests, json

password = 'SOD2018'

def led(id=0, status=0):
    return _executa('led', [id, status])

def alarme(status=0):
    return _executa('alarme', [status])

def temperatura(status=0):
    return _executa('temperatura', [status])

def _executa(method, params):
    data_cript = _criptografar({
                    'method': method,
                    'params': params
                })

    try:
        requests.post('http://192.168.1.103:5000', data=data_cript)

    except NewConnectionError:
        return json.dumps({'status': False})

    return json.dumps({'status': True})

def _criptografar(data):
    data = json.dumps(data)
    return encrypt(password, data)
