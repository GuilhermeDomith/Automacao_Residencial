from simplecrypt import encrypt
import requests, json

password = 'SOD2018'

def led(self, id=0, status=0):
    _executa('led', [id, status])

def alarme(self, status=0):
    _executa('alarme', [status])

def temperatura(self, status=0):
    _executa('temperatura', [status])

def _executa(method, params):
    data_cript = _criptografar({
                    'method': method,
                    'params': params
                })
                
    requests.post('http://localhost:8000/', data=data_cript)

def _criptografar(data):
    data = json.dumps(data)
    return encrypt(password, data)
