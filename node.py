import time
import json
from random import randrange
import paho.mqtt.client as mqtt

def get_fake_sensor_data():
    return {
        'temperature': randrange(10),
        'humidity': randrange(10),
        'pressure': randrange(10),
    }

broker_url = "localhost"
broker_port = 9001

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))
    client.subscribe("weather_station/request_data")

def handle_request_data(client, userdata, message):
    if message.payload.decode() == "start_measuring":
        subscribe_and_publish(client)
    elif message.payload.decode() == "stop_measuring":
        unsubscribe(client)

def subscribe_and_publish(client):
    client.subscribe("weather_station/sensor_data")
    sensor_data = get_fake_sensor_data()
    client.publish("weather_station/sensor_data", json.dumps(sensor_data))
    print(json.dumps(sensor_data))

def unsubscribe(client):
    client.unsubscribe("weather_station/sensor_data")

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    #print("Received MQTT message:")
    #print("Topic:", topic)
    #print("Payload:", payload)

    if topic == "weather_station/sensor_data":
        subscribe_and_publish(client)

def on_publish(client, userdata, mid):
    print("Message published with MID: " + str(mid))

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with result code: " + str(rc))

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
