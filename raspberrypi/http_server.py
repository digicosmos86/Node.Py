## first run sudo python3 pip install --upgrade flask
## export FLASK_APP=http_server.py
## python3 -m flask run host=0.0.0.0

from flask import Flask, jsonify
from sense_hat import SenseHat
sense = SenseHat()
app = Flask(__name__)

@app.route("/")
def all():
    return jsonify(
        temperature=round(sense.get_temperature(),1),
        humidity=round(sense.get_humidity(),1),
        pressure=round(sense.get_pressure(),1)
    )

@app.route("/temperature")
def temp():
    return str(round(sense.get_temperature(),1))

@app.route("/humidity")
def humidity():
    return str(round(sense.get_humidity(), 1))

@app.route("/pressure")
def pressure():
    return str(round(sense.get_pressure(), 1))
