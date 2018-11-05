"""
    Módulo para comunicação com o arduíno via bluetooth.
"""

def led(status=False):
    pass

def alarme(status=False, sensibilidade=100):
    pass

def ventilador(status=False, potencia=100):
    pass

comandos = {
    'led': led,
    'alarme': alarme,
    'ventilador': ventilador
}