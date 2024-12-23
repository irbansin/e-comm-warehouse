
import pandas as pd
from flask import Flask, render_template, request, jsonify 
import os

from startetl import startETL



app = Flask(__name__)

etlRunning = False

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/startetl')
def startetl(): 
    status = startETL()
    return jsonify({'message': status}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
