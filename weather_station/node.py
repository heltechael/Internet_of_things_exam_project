import asyncio
import json
from random import randrange
import paho.mqtt.client as mqtt

# Import classes
from measurement import Measurement

class Node:
    def __init__(self, broker_url = "192.168.217.240", broker_port = 9001):
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        self.client.message_callback_add("weather_station/request_data", self.handle_request_data)
        self.active_sensors = set()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    async def get_sensor_data(self, sensor_type):
        while sensor_type in self.active_sensors:
            measurement = Measurement(sensor_type)
            self.client.publish(f"weather_station/{sensor_type}", json.dumps(measurement.to_dict()))
            print(json.dumps(measurement.to_dict()))
            await asyncio.sleep(1)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker on node.py with result code: " + str(rc))
        self.client.subscribe("weather_station/request_data")

    def handle_request_data(self, client, userdata, message):
        payload = message.payload.decode()
        sensor_type = payload.split(':')[1]

        # Start
        if payload.startswith("start"):
            print(f"Starting measurements for {sensor_type}!")
            self.active_sensors.add(sensor_type)
            asyncio.run_coroutine_threadsafe(self.get_sensor_data(sensor_type), self.loop)

        # Stop
        elif payload.startswith("stop"):
            print(f"Stopping measurements for {sensor_type}!")
            self.active_sensors.remove(sensor_type)

    def on_message(self, client, userdata, message):
        pass

    def on_publish(self, client, userdata, mid):
        print("Message published with MID: " + str(mid))

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT broker with result code: " + str(rc))

    def run(self):
        self.client.connect(self.broker_url, self.broker_port)
        self.client.loop_start()
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        self.client.loop_stop()
        self.client.disconnect()

if __name__ == "__main__":
    node = Node()
    node.run()
