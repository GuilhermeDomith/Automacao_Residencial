from flask import Flask, request, render_template
from source.comodos import SalaEstar, Cozinha
import comandos_rpc
import json

app = Flask(__name__)

rooms = {
    'sala_star' : SalaEstar(),
    'cozinha': Cozinha()
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', rooms=rooms )

@app.route('/component/<key>', methods=['GET'])
def component(key):
    return render_template('component.html', component=rooms[key].components )

@app.route('/requisicao', methods=['POST'])
def requisicao():
    id = request.form['id']
    status = request.form['status']
    comandos_rpc.led(id, status)

if __name__ == '__main__':
    app.run(debug=True,  host='192.168.1.125', port=5000)
