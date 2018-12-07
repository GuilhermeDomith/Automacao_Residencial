"""
    Módulo para comunicação com o arduíno via bluetooth.
"""
import bluetooth
import sys
import time
import socket
import json

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


        self.sock.settimeout(120)
        self.comandos = {
            'led': self.led,
            'alarme': self.alarme,
            'modo_automatico': self.modo_automatico, 
            'consulta_status_automatico': self.consulta_status_automatico,
            'consulta_status_alarme': self.consulta_status_alarme,
            'consulta_status_led': self.consulta_status_led
       }


    def consulta_status_automatico(self):
        self.sock.settimeout(120)
        self.sock.send('SM')

        data = ''

        try:
            while True:
                data = self.sock.recv(1024)
            
                data = data.decode('utf-8')

                if data:
                    if data != '\r\n':
                        print("#### => {}".format(data))
                        break

            return json.dumps({'status': data})

        except Exception:
            return json.dumps({'erro': 'Falha na comunicação com o Bluetooth'})

    def consulta_status_alarme(self):
        self.sock.settimeout(120)
        self.sock.send('SA')

        data = ''

        try:
            while True:
                data = self.sock.recv(2048)
            
                data = data.decode('utf-8')

                if data:
                    if data != '\r\n':
                        print("#### => {}".format(data))
                        break

            return json.dumps({'status': data})

        except Exception:
            return json.dumps({'erro': 'Falha na comunicação com o Bluetooth'})

    def consulta_status_led(self, id=0):
        self.sock.settimeout(120)
        print(id)
        consulta = 'SL' + str(id)
        print("CONSULTA >> %s" % str(consulta))
        self.sock.send(consulta)

        data = ''

        try:
            while True:
                data = self.sock.recv(2048)

                data = data.decode('utf-8')

                if data:
                    if data != '\r\n':
                        print("#### => {}".format(data))
                        break

            print("Status: %s" % str(data))

            return json.dumps({'status': data})
        except Exception:
            return json.dumps({'erro': 'Falha na comunicação com o Bluetooth'})

    def led(self, id=0, status=0):
        try:
            self.sock.send('L%s%s'%(id, status))
            return json.dumps({'status': 'OK'})
        except Exception:
            return json.dumps({'status': 'ERROR'})

    def alarme(self, status=0):
        try:
            self.sock.send('A%s'%status)
            return json.dumps({'status': 'OK'})
        except Exception:
            return json.dumps({'status': 'ERROR'})

    def modo_automatico(self, status=0):
        try:
            self.sock.send('M%s'%status)
            return json.dumps({'status': 'OK'})
        except Exception:
            return json.dumps({'status': 'ERROR'})

    def executa(self, method, params):
        return self.comandos[method](*params)
        

    def encerrar_conexao(self):
        self.sock.close()