import time
import json
from random import randrange
import paho.mqtt.client as mqtt

temp = 0
humid = 0
press = 0

# Define callback functions
def on_connect_to_pi(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe("pc/temperature")  # Subscribe to the topic where Raspberry Pi publishes temperature data
    client.subscribe("pc/humidity")
    client.subscribe("pc/pressure")
    
def on_message_to_pi(client, userdata, msg):
    global temp, humid, press
    
    if msg.topic == "pc/temperature":
        temp = float(msg.payload.decode())
    if msg.topic == "pc/humidity":
        humid = float(msg.payload.decode())
    if msg.topic == "pc/pressure":
        press = float(msg.payload.decode())
    
    print("Received temperature:", temp)
    print("Received humidity:", humid)
    print("Received pressure:", press)
# Create an MQTT client instance
clientPi = mqtt.Client()

# Configure the callbacks
clientPi.on_connect = on_connect_to_pi
clientPi.on_message = on_message_to_pi

# Connect to the MQTT broker
broker_address = "localhost"
broker_portPi = 9001
clientPi.connect(broker_address, broker_portPi)

# Start the MQTT loop to listen for messages
clientPi.loop_start()


def get_fake_sensor_data():
<<<<<<< Updated upstream
=======
    time.sleep(3)
    global temp
>>>>>>> Stashed changes
    return {
        'temperature': temp,
        'humidity': humid,
        'pressure': press,
    }

broker_url = "localhost"
broker_port = 8001

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
