from Crypto.Cipher import AES
import requests, json, random, string, config, time

cripto = AES.new(config.password_cripto)

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

    except requests.ConnectionError as ce:
        return json.dumps({'status': False, 'message': 'Servidor não conectado'})

    except Exception as e:
        return json.dumps({'status': False, 'message': str(e)})

def _criptografar(data):
    # Adiciona o caractere para separar o git dos dados.
    data = json.dumps(data) + '#'
    resto = len(data) % 16

    # Verifica se o tamanho é multiplo de 16,
    # se não adiciona caracteres para que seja.
    if resto > 0:
        data = data + ''.join([random.choice(string.ascii_letters) for n in range(16 - resto)])

    return cripto.encrypt(data)
