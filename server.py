"""
Internet of Things exam project: Weather Station
Made by: Anisa Nuur, Dilan Celebi, and Michael Noerbo
"""

from flask import Flask, render_template, make_response, g, request, send_file
from flask_mqtt import Mqtt

import logging
from utils import is_raspberry_pi

# Instantiate the Flask app
app = Flask(__name__)

# Configure Flask-MQTT
app.config['MQTT_BROKER_URL'] = 'localhost'  # Set the MQTT broker URL (the IP address or hostname of your Raspberry Pi)
app.config['MQTT_BROKER_PORT'] = 9001  # Set the MQTT broker port (the port number your Raspberry Pi is listening on)
app.config['MQTT_USERNAME'] = 'username'  # Set the username for MQTT authentication (if applicable)
app.config['MQTT_PASSWORD'] = 'password'  # Set the password for MQTT authentication (if applicable)

mqtt = Mqtt(app)  # Instantiate Flask-MQTT

@app.route('/')
def index():
    return render_template('index.html')

# MQTT subscription callback
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    print("Received MQTT message:")
    print("Topic:", topic)
    print("Payload:", payload)

@app.route('/button/<int:button_number>', methods=['POST'])
def button(button_number):

    return_message = ""

    match button_number:
        case 1:
            # start measurin
            return_message = "Button 1: Hello world!"
        case 2:
            return_message = "Button 2 pressed!"
        case 3:
            return_message = "Button 3 pressed!"
        case 4:
            return_message = "Button 4 pressed!"

    print(return_message)
    return make_response({'message': return_message}, 200)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return make_response({'message': 'Hello World!'}, 200)

@app.route('/statistics', methods=['GET'])
def getStatistics():
    stats = [1,2,3,4,5]
    return make_response(stats, 200)

@app.errorhandler(500)
def server_error(e):
    logging.exception("Internal error: %s", e)
    return make_response({"error": str(e)}, 500)

# Start the Flask app 
host_local_computer = "localhost"   # Listen for connections on the local computer
host_local_network = "0.0.0.0"      # Listen for connections on the local network
app.run(host=host_local_network if is_raspberry_pi() else host_local_computer, port=9000)