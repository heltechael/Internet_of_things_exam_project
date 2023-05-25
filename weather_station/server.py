from flask import Flask, render_template, make_response, g, request, send_file
from flask_mqtt import Mqtt
from flask_cors import CORS
from flask_socketio import SocketIO
from random import randrange
import logging
import json
from json import loads, JSONDecodeError
import sqlite3

# import classes
from .measurement import Measurement

class Server:
    def __init__(self):
        # Instantiate the Flask app
        self.app = Flask(__name__)
        CORS(self.app)
        self.socketio = SocketIO(self.app)

        # Configure Flask-MQTT
        self.app.config['MQTT_BROKER_URL'] = 'localhost'
        self.app.config['MQTT_BROKER_PORT'] = 9001

        self.mqtt = Mqtt(self.app)  # Instantiate Flask-MQTT

        # Connect methods
        @self.mqtt.on_connect()
        def handle_mqtt_connect(client, userdata, flags, rc):
            print("Connected to MQTT broker in server.py")
            self.mqtt.subscribe("weather_station/+")

        @self.mqtt.on_subscribe()
        def handle_mqtt_subscribe(client, userdata, mid, granted_qos):
            print("Subscribed to weather_station/+ in server.py")

        @self.mqtt.on_message()
        def handle_mqtt_message(client, userdata, message):
            print("Received message: ", message.payload.decode())
            data = message.payload.decode()
            try:
                data_dict = json.loads(data)
                measurement = Measurement.from_dict(data_dict)
                self.socketio.emit('mqtt_message', measurement.to_dict())

                # Store in DB:
                # Database connection and insert
                with self.app.app_context():
                    conn = self.get_db()
                    c = conn.cursor()
                    c.execute("INSERT INTO measurements (sensor_id, value, timestamp) VALUES (?, ?, ?)",
                            (measurement.sensor_id, measurement.value, measurement.timestamp))
                    conn.commit()
            except JSONDecodeError:
                pass

        self.app.route('/')(self.index)
        self.app.route('/hello', methods=['GET', 'POST'])(self.hello)
        self.app.route('/button/<string:action>/<string:sensor_type>', methods=['POST'])(self.button)
        self.app.errorhandler(500)(self.server_error)
        self.socketio.on('client_connect')(self.handle_my_custom_event)

        self.init_db()

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect('database2.db')
        return db

    def close_connection(self, exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def init_db(self):
        with self.app.app_context():
            db = self.get_db()
            c = db.cursor()
            c.execute("DROP TABLE IF EXISTS measurements")
            with self.app.open_resource('schema.sql', mode='r') as f:
                c.executescript(f.read())
            db.commit()

    def handle_mqtt_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker in server.py")
        self.mqtt.subscribe("weather_station/temperature")
        self.mqtt.subscribe("weather_station/humidity")
        self.mqtt.subscribe("weather_station/pressure")
        self.mqtt.subscribe("weather_station/+")

    def handle_mqtt_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed to weather_station/+ in server.py")

    def handle_mqtt_message(self, client, userdata, message):
        print("Received message: ", message.payload.decode())
        data = message.payload.decode()
        try:
            data_dict = json.loads(data)
            measurement = Measurement.from_dict(data_dict)
            self.socketio.emit('mqtt_message', measurement.to_dict())

            # Store in DB:
            # Database connection and insert
            with self.app.app_context():
                conn = self.get_db()
                c = conn.cursor()
                c.execute("INSERT INTO measurements (sensor_id, value, timestamp) VALUES (?, ?, ?)",
                        (measurement.sensor_id, measurement.value, measurement.timestamp))
                conn.commit()
        except JSONDecodeError:
            pass

    def index(self):
        return render_template('index.html')

    def hello(self):
        return make_response({'message': 'Hello World!'}, 200)
    
    def button(self, action, sensor_type):
        if action not in ['start', 'stop']:
            return make_response({'message': 'Invalid action'}, 400)

        if sensor_type not in ['temperature', 'humidity', 'pressure']:
            return make_response({'message': 'Invalid sensor type'}, 400)

        self.mqtt.publish("weather_station/request_data", f"{action}:{sensor_type}")

        return_message = f"{action.capitalize()} measurement for {sensor_type}!"
        print(return_message)
        return make_response({'message': return_message}, 200)

    def server_error(self, e):
        logging.exception("Internal error: %s", e)
        return make_response({"error": str(e)}, 500)

    def handle_my_custom_event(self, json):
        print('received json: ' + str(json))

    def run(self):
        host_local_computer = "localhost"   # Listen for connections on the local computer
        host_local_network = "0.0.0.0"      # Listen for connections on the local network
        self.socketio.run(self.app, allow_unsafe_werkzeug=True, host=host_local_network if False else host_local_computer, port=9000)

if __name__ == "__main__":
    server = Server()
    server.run()