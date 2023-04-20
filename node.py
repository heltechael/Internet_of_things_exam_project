from utils import is_raspberry_pi
import paho.mqtt.client as mqtt

# Define the MQTT broker URL, port, and optional username/password for authentication
broker_url = "localhost"  # Replace with the IP address or hostname of your Flask application
broker_port = 9001  # Replace with the port number your Flask application is listening on
username = None  # Replace with the username for MQTT authentication (if applicable)
password = None  # Replace with the password for MQTT authentication (if applicable)

# Define the callback functions for MQTT events
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))

def on_publish(client, userdata, mid):
    print("Message published with MID: " + str(mid))

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with result code: " + str(rc))

# Instantiate the MQTT client
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# Connect to the MQTT broker
client.connect(broker_url, broker_port)

# Publish a message
topic = "my_topic"  # Replace with the topic you want to publish to
payload = "Hello from Python!"  # Replace with the payload you want to publish
client.publish(topic, payload)

# Wait for any published messages to be sent and acknowledged
client.loop()

# Disconnect from the MQTT broker
client.disconnect()