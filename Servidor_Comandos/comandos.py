"""
    Módulo para comunicação com o arduíno via bluetooth.
"""
import bluetooth
import sys
import time
import socket

class HomeControl():

    def __init__(self, bt_addr):
        self.port = 1
        self.bt_addr = bt_addr

        # Executa tentativas de conexão com o bluetooth
        while True:
            try:
                self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                self.sock.connect((bt_addr, self.port))
                print('Bluetooth Conectado...')
                break
            except bluetooth.btcommon.BluetoothError as e:
                print("Erro ao conectar Bluetooth. %s" %e)
                self.sock.close()
                time.sleep(5)
                continue


        self.sock.settimeout(1.0)
        self.comandos = {
            'led': self.led,
            'alarme': self.alarme,
            'modo_automatico': self.modo_automatico
       }


    def led(self, id=0, status=0):
        self.sock.send('L%s%s'%(id, status))

    def alarme(self, status=0):
        self.sock.send('A%s'%status)

        while True:
            data = self.sock.recv(1024)

            if data:
                print("#### => {}".format(data))
                break

    def modo_automatico(self, status=0):
        self.sock.send('M%s'%status)

    def executa(self, method, params):
        self.comandos[method](*params)

    def encerrar_conexao(self):
        self.sock.close()
