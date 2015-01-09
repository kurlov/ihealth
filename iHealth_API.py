from flask import Flask, redirect
from iHealth import iHealth
import config as cfg

app = Flask(__name__)
client_id = cfg.CLIENT_ID
client_secret = cfg.CLIENT_SECRET
callback = cfg.CALLBACK_URI
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
def api_bp():
    r = api.get_blood_pressure()
    return r

@app.route('/api_weight')
def api_weight():
    r = api.get_weight()
    return r

@app.route('/api_bg')
def api_bg():
    r = api.get_bg()
    return r

@app.route('/api_blood_oxygen')
def api_blood_oxygen():
    r = api.get_blood_oxygen()
    return r

@app.route('/api_activity_report')
def api_activity_report():
    r = api.get_activity_report()
    return r

@app.route('/api_sleep_report')
def api_sleep_report():
    r = api.get_sleep_report()
    return r

@app.route('/api_food')
def api_food():
    r = api.get_food()
    return r

@app.route('/api_sport_report')
def api_sport_report():
    r = api.get_sport_report()
    return r

if __name__ == '__main__':
    app.run(debug=True)
