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

    try:
        for i in range(len(rooms[key].components)):
            resp = consulta(rooms[key].components[i]['pin'])

            status = json.loads(resp)['status']

            print("## Status => " + status)
            rooms[key].components[i]['status'] = int(status)

            print("## {}".format(rooms[key].components[i]['status']))

            if status == False:
                pass

    except json.JSONDecodeError as excJson:
        print(excJson)

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

# @app.route('/consulta', methods=['POST'])
def consulta(id):
    if id == 'alarme':
        return comandos_rpc.consulta_status_alarme()
    elif id == 'modo_automatico':
        return comandos_rpc.consulta_status_automatico()
    else:
        return comandos_rpc.consulta_status_led(id)

if __name__ == '__main__':
    app.run(debug=True,  host=config.servidor_app, port=config.porta_sapp)
