import time
import json
from random import randrange
import paho.mqtt.client as mqtt

# Import classes
from .measurement import Measurement

class Node:
    def __init__(self, broker_url="localhost", broker_port=9001):
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        self.client.message_callback_add("weather_station/request_data", self.handle_request_data)

    def get_fake_sensor_data(self):
        time.sleep(1)
        return {
            'temperature': Measurement("temperature", randrange(10)),
            'humidity': Measurement("humidity", randrange(10)),
            'pressure': Measurement("pressure", randrange(10)),
        }

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker on node.py with result code: " + str(rc))
        self.client.subscribe("weather_station/request_data")

    def handle_request_data(self, client, userdata, message):
        payload = message.payload.decode()
        sensor_type = payload.split(':')[1]

        # Start
        if payload.startswith("start"):
            print(f"Starting measurements for {sensor_type}!")
            self.subscribe(client, sensor_type)

        # Stop
        elif payload.startswith("stop"):
            print(f"Stopping measurements for {sensor_type}!")
            self.unsubscribe(client, sensor_type)

    def subscribe(self, client, sensor_type):
        client.subscribe(f"weather_station/{sensor_type}")
        self.publish_sensor_data(client, sensor_type)

    def unsubscribe(self, client, sensor_type):
        client.unsubscribe(f"weather_station/{sensor_type}")

    def publish_sensor_data(self, client, sensor_type):
        sensor_data = self.get_fake_sensor_data()[sensor_type]
        client.publish(f"weather_station/{sensor_type}", json.dumps(sensor_data.to_dict()))
        print(json.dumps(sensor_data.to_dict()))

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode()
        if "weather_station/" in topic:
            sensor_type = topic.split('/')[1]
            self.publish_sensor_data(client, sensor_type)

    def on_publish(self, client, userdata, mid):
        print("Message published with MID: " + str(mid))

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT broker with result code: " + str(rc))

    def run(self):
        self.client.connect(self.broker_url, self.broker_port)
        self.client.loop_start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        self.client.loop_stop()
        self.client.disconnect()

if __name__ == "__main__":
    node = Node()
    node.run()