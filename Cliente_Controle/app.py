from flask import Flask, request, render_template
from source.comodos import SalaEstar, Cozinha, Copa, Quarto, Components
import comandos_rpc, json, config

app = Flask(__name__)

nameApp = "Home"
rooms = {
    'sala_star' : SalaEstar(),
    'cozinha': Cozinha(),
    'copa': Copa(),
    'quarto': Quarto(),
    'components': Components()
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', rooms=rooms, title=nameApp )

@app.route('/component/<key>', methods=['GET'])
def component(key):
    return render_template('component.html', component=rooms[key].components, title=rooms[key]._name )

@app.route('/requisicao', methods=['POST'])
def requisicao():
    id = request.form['id']
    status = request.form['status']

    if id == 'alarme':
        return comandos_rpc.alarme(status)
    elif id == 'modo_automatico':
        return comandos_rpc.modo_automatico(status)
    else:
        return comandos_rpc.led(id, status)

if __name__ == '__main__':
    app.run(debug=True,  host=config.servidor_app, port=config.porta_sapp)
