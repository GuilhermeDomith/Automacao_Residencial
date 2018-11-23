from Crypto.Cipher import AES
import requests, json, random, string

password = 'SOD-2018SOD-2018'
cripto = AES.new(password)

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
    # Adiciona o caractere para separar o git dos dados.
    data = json.dumps(data) + '#'
    resto = len(data) % 16

    # Verifica se o tamanho é multiplo de 16, 
    # se não adiciona caracteres para que seja.
    if resto > 0:
        data = data + ''.join([random.choice(string.ascii_letters) for n in range(16 - resto)])

    return cripto.encrypt(data)