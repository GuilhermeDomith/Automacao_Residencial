from Crypto.Cipher import AES
from base64 import b64encode
import requests, json, random, string, config, time

passwd_criptografar = "sistemasdistribuidos2018"

def consulta_status_led(id):
    return _executa('consulta_status_led', [id])

def consulta_status_alarme():
    return _executa('consulta_status_alarme', [])

def consulta_status_automatico():
    return _executa('consulta_status_automatico', [])

def led(id=0, status=0):
    return _executa('led', [id, status])

def alarme(status=0):
    return _executa('alarme', [status])

def modo_automatico(status=0):
    return _executa('modo_automatico', [status])

def _executa(method, params):
    data_cript = _criptografar({
                    'method': method,
                    'params': params
                })

    try:
        resp = requests.post('http://{}:{}'.format(config.servidor_rpc, config.porta_srpc), data=data_cript)
        # print(resp.text)
        return resp.text

    except requests.ConnectionError:
        return json.dumps({'status': False, 'message': 'Servidor não conectado'})

    except Exception as e:
        return json.dumps({'status': False, 'message': str(e)})

def _criptografar(data):
    data_send = {}
    cripto = AES.new(passwd_criptografar.encode(), AES.MODE_EAX)    

    data_cript = cripto.encrypt(json.dumps(data).encode())
    data_send['data'] = b64encode(data_cript).decode()
    data_send['nonce'] = b64encode(cripto.nonce).decode()

    return data_send
