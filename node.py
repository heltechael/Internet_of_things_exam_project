import time
import json
from random import randrange
import paho.mqtt.client as mqtt
from datetime import datetime
from measurement import Measurement

def get_fake_sensor_data():
    time.sleep(1)
    
    return {
        'temperature': Measurement("temperature", randrange(10)),
        'humidity': Measurement("humidity", randrange(10)),
        'pressure': Measurement("pressure", randrange(10)),
    }

broker_url = "localhost"
broker_port = 9001

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker on node.py with result code: " + str(rc))
    client.subscribe("weather_station/request_data")

def handle_request_data(client, userdata, message):
    payload = message.payload.decode()
    sensor_type = payload.split(':')[1]

    # Start
    if payload.startswith("start"):
        print(f"Starting measurements for {sensor_type}!")
        subscribe(client, sensor_type)

    # Stop
    elif payload.startswith("stop"):
        print(f"Stopping measurements for {sensor_type}!")
        unsubscribe(client, sensor_type)

def subscribe(client, sensor_type):
    client.subscribe(f"weather_station/{sensor_type}")
    publish_sensor_data(client, sensor_type)

def unsubscribe(client, sensor_type):
    client.unsubscribe(f"weather_station/{sensor_type}")

def publish_sensor_data(client, sensor_type):
    sensor_data = get_fake_sensor_data()[sensor_type]
    client.publish(f"weather_station/{sensor_type}", json.dumps(sensor_data.to_dict()))
    print(json.dumps(sensor_data.to_dict()))

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    if "weather_station/" in topic:
        sensor_type = topic.split('/')[1]
        publish_sensor_data(client, sensor_type)

def on_publish(client, userdata, mid):
    print("Message published with MID: " + str(mid))

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with result code: " + str(rc))

# Connect methods
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_disconnect = on_disconnect

client.message_callback_add("weather_station/request_data", handle_request_data)

client.connect(broker_url, broker_port)

client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()