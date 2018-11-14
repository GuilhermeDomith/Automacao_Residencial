from flask import Flask, request, render_template
import json




app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,  host='192.168.1.126', port=5000)

