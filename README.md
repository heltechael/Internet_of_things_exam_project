# Weather Station Project

Exam project for Internet of Things course at AU 2023.

Members:
- Anisa Nuur
- Dilan Celebi
- Michael Nørbo

## Installation
1) Navigate to root directory
1) Install dependencies with <code>python setup.py install</code>.

## Run the MQTT broker using Mosquitto
1) Make sure an MQTT broker is installed (e.g. Mosquitto)
2) Open terminal and start mosquitto: </code>mosquitto -p 9001</code>.

## Run Server and Node
1) Run server: open new terminal in root directory <code>python server.py</code>.
2) Open new terminal and connect nodes: <code>python node.py</code>.

## Making sure everything works locally
1) In terminal
   1) Type <code>curl http://localhost:9000/hello</code>.
   2) If message <code>Hello World!</code> is received, the server is started correctly.
2) In browser
   1) Type <code>http://localhost:9000/hello</code> in browser.
   2) If index page is loaded, server is started correctly.