"""
Internet of Things exam project: Weather Station
Made by: Anisa Nuur, Dilan Celebi, and Michael Noerbo
"""

from flask import Flask, render_template, make_response, g, request, send_file
from flask_mqtt import Mqtt
from flask_cors import CORS
from flask_socketio import SocketIO
from measurement import Measurement
from random import randrange
import logging
import json
from utils import is_raspberry_pi
from json import loads, JSONDecodeError
import sqlite3

# Instantiate the Flask app
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Configure Flask-MQTT
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 9001

mqtt = Mqtt(app)  # Instantiate Flask-MQTT

#Sqllite database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database2.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        c = db.cursor()
        c.execute("DROP TABLE IF EXISTS measurements")
        with app.open_resource('schema.sql', mode='r') as f:
            c.executescript(f.read())
        db.commit()

@mqtt.on_connect()
def handle_mqtt_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker in server.py")
    mqtt.subscribe("weather_station/temperature")
    mqtt.subscribe("weather_station/humidity")
    mqtt.subscribe("weather_station/pressure")
    mqtt.subscribe("weather_station/+")

@mqtt.on_subscribe()
def handle_mqtt_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to weather_station/+ in server.py")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print("Received message: ", message.payload.decode())
    data = message.payload.decode()
    try:
        data_dict = json.loads(data)
        measurement = Measurement.from_dict(data_dict)
        socketio.emit('mqtt_message', measurement.to_dict())

        # Store in DB:
        # Database connection and insert
        with app.app_context():
            conn = get_db()
            c = conn.cursor()
            c.execute("INSERT INTO measurements (sensor_id, value, timestamp) VALUES (?, ?, ?)",
                    (measurement.sensor_id, measurement.value, measurement.timestamp))
            conn.commit()
    except JSONDecodeError:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return make_response({'message': 'Hello World!'}, 200)

@app.route('/button/<string:action>/<string:sensor_type>', methods=['POST'])
def button(action, sensor_type):
    if action not in ['start', 'stop']:
        return make_response({'message': 'Invalid action'}, 400)

    if sensor_type not in ['temperature', 'humidity', 'pressure']:
        return make_response({'message': 'Invalid sensor type'}, 400)

    mqtt.publish("weather_station/request_data", f"{action}:{sensor_type}")

    return_message = f"{action.capitalize()} measurement for {sensor_type}!"
    print(return_message)
    return make_response({'message': return_message}, 200)

@app.errorhandler(500)
def server_error(e):
    logging.exception("Internal error: %s", e)
    return make_response({"error": str(e)}, 500)

@socketio.on('client_connect')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

# Start the Flask app
init_db() 
host_local_computer = "localhost"   # Listen for connections on the local computer
host_local_network = "0.0.0.0"      # Listen for connections on the local network
socketio.run(app, allow_unsafe_werkzeug=True, host=host_local_network if is_raspberry_pi() else host_local_computer, port=9000)

