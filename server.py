"""
Internet of Things exam project: Weather Station
Made by: Anisa Nuur, Dilan Celebi, and Michael Noerbo
"""

from flask import Flask, render_template, make_response, g, request, send_file
from flask_mqtt import Mqtt
from flask_cors import CORS

import logging
import json
from utils import is_raspberry_pi

# Instantiate the Flask app
app = Flask(__name__)
CORS(app)

# Configure Flask-MQTT
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 9001
#app.config['MQTT_USERNAME'] = 'username'
#app.config['MQTT_PASSWORD'] = 'password'

mqtt = Mqtt(app)  # Instantiate Flask-MQTT

received_data = []

@mqtt.on_connect()
def handle_mqtt_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker in server.py")
    mqtt.subscribe("weather_station/sensor_data")

@mqtt.on_subscribe()
def handle_mqtt_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to weather_station/sensor_data in server.py")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global received_data
    topic = message.topic
    payload = message.payload.decode()

    #print("Received MQTT message:")
    #print("Topic:", topic)
    #print("Payload:", payload)

    data = json.loads(payload)
    received_data.append(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button/<int:button_number>', methods=['POST'])
def button(button_number):
    if button_number == 1:
        mqtt.publish("weather_station/request_data", "start_measuring")
    elif button_number == 2:
        mqtt.publish("weather_station/request_data", "stop_measuring")
    return_message = f"Button {button_number} pressed!"
    print(return_message)
    return make_response({'message': return_message}, 200)

@app.route('/sensor_data', methods=['GET'])
def sensor_data():
    global received_data
    return make_response({'sensor_data': received_data}, 200)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return make_response({'message': 'Hello World!'}, 200)

@app.errorhandler(500)
def server_error(e):
    logging.exception("Internal error: %s", e)
    return make_response({"error": str(e)}, 500)

# Start the Flask app 
host_local_computer = "localhost"   # Listen for connections on the local computer
host_local_network = "0.0.0.0"      # Listen for connections on the local network
app.run(host=host_local_network if is_raspberry_pi() else host_local_computer, port=9000)