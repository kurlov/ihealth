from flask import Flask, redirect
from iHealth import iHealth
import config

app = Flask(__name__)
client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
callback = config.CALLBACK_URI
api = iHealth(client_id, client_secret, callback)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/authorize')
def authorize():
    r = api.authorize()
    return redirect(r.url)

@app.route('/callback')
def callback():
    r = api.callback()
    return r

@app.route('/api_bp')
def call_api_bp():
    r = api.get_blood_pressure()
    return r

@app.route('/api_weight')
def call_api_weight():
    r = api.get_weight()
    return r

if __name__ == '__main__':
    app.run(debug=True)
