# Weather Station Project

Exam project for Internet of Things course at AU 2023.

Members:
- Anisa Nuur
- Dilan Celebi
- Michael Nørbo

## Installation
1) Navigate to root directory
1) Install dependencies with <code>pip -r install requirements.txt</code>.

## Run the MQTT broker using Mosquitto
1) Make sure an MQTT broker is installed (e.g. Mosquitto)
2) Open terminal and navigate to the mosquitto directory (e.g. <code>/usr/share/doc/mosquitto/examples/</code>)
3) Start mosquitto: <code>mosquitto -c /mosquitto.conf -v</code>.

## Run Server and Node
1) Run server: open new terminal in root directory <code>python -m weather_station.server</code>.
2) Open new terminal and connect nodes: <code>python -m weather_station.node</code>.

## Making sure the server works
1) In terminal: <code>python -m weather_station.test.test_server</code>.

## Making sure the web app works
1) Navigate to browser and enter the url: </code>http://localhost:9000/</code>.