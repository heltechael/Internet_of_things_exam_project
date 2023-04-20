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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button/<int:button_number>', methods=['POST'])
def button(button_number):

    return_message = ""

    match button_number:
        case 1:
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