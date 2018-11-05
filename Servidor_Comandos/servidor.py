from flask import Flask, request
from comandos import comandos
import json

app = Flask(__name__)

@app.route('/', method=['GET'])
def comando_residencia():
    RPC = json.dumps(request.form['RPC'])
    comandos[RPC['method']](RPC['args'])
