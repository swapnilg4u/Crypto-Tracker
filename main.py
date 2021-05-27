import json
from logging import debug
import os
from datetime import datetime
import time
import pytz
import requests
from flask import Flask, Response, render_template

app = Flask(__name__)
API_URL = "https://x.wazirx.com/wazirx-falcon/api/v2.0/crypto_rates"

@app.route('/')
def home():
    supported_cryptos = requests.get(API_URL).json().keys()
    return render_template('home.html', supported_cryptos=supported_cryptos)

@app.route('/<crypto>')
def index(crypto):
    supported_cryptos=requests.get(API_URL).json().keys()
    if crypto.lower() in supported_cryptos:
        return render_template('index.html',crypto=crypto)
    return "This Crypto is not yet supported :("

@app.route('/chart-data/<crypto>')
def chart_data(crypto):
    def generate_data(crypto):
        while True:
            price = requests.get(API_URL).json()[crypto.lower()]['inr']
            json_data = json.dumps(
                {
                    'time': datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S'),
                    'value': price
                }
            )
            yield f"data:{json_data}\n\n"
            time.sleep(15)

    return Response(generate_data(crypto), mimetype='text/event-stream')


if __name__=='__main__':
    app.run(host='0.0.0.0',port='8080',threaded=True)