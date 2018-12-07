from flask import Flask, request, render_template
from source.comodos import SalaEstar, Cozinha, Copa, Quarto, Casa
import comandos_rpc, json, config

app = Flask(__name__)

nameApp = "Home"
rooms = {
    'sala_star' : SalaEstar(),
    'cozinha': Cozinha(),
    'copa': Copa(),
    'quarto': Quarto(),
    'casa': Casa()
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', rooms=rooms, title=nameApp )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',  title=nameApp), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', error=e, title=nameApp), 500

@app.route('/component/<key>', methods=['GET'])
def component(key):

    if not key in rooms:
        return render_template('404.html'), 404

    try:
        for i in range(len(rooms[key].components)):
            resp = consulta(rooms[key].components[i]['pin'])

            status = json.loads(resp)['status']

            rooms[key].components[i]['status'] = int(status)

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
    app.run(host=config.servidor_app, port=config.porta_sapp)
