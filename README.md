# Weather Station Project

Exam project for Internet of Things course at AU 2023.

Members:
- Anisa Nuur
- Dilan Celebi
- Michael Nørbo

## Installation
1) Install dependencies with <code>pip install -r requirements</code>.

## Running 
1)Connect the Rasberry pi to a screen and get the ip address
2)Connect to the main computer with ssh
3)From the computer after connecting the pi, open the mqtt_test.py and change the ip address to computer address that you want to connect, save and exit.
4)The next steps are for the main computer:
5)Find the Mosquitto main configuration file by running the following command: <code>sudo find / -name mosquitto.conf 2>/dev/null</code> Note down the directory where the mosquitto.conf file is located. In this example, let's assume it is /usr/share/doc/mosquitto/examples.
6)Open the mosquitto.conf file for editing using the nano text editor: <code>sudo nano /usr/share/doc/mosquitto/examples/mosquitto.conf</code>. Note:I added my own path. Don't forget to change it to yours.
7)Inside the configuration file, add the following lines to configure the MQTT broker:<code>listener 9001</code> below of it add that <code>allow_anonymous true</code>
8)Save the changes and exit the nano editor
9)Run the Mosquitto MQTT broker with the updated configuration file: <code>mosquitto -c /usr/share/doc/mosquitto/examples/mosquitto.conf -v </code>
10)Also open a new terminal and start another mosquitto to run the server connection between another node: <code>mosquitto -p 9001</code>.
11)Open new terminal and start server: <code>python server.py</code>.
12)Open new terminal and connect nodes: <code>python node.py</code>.
13)Run the mqtt_test.py file inside of the Rasberry Pi to send the data.

## Making sure everything works locally
1) In terminal
   1) Type <code>curl http://localhost:9000/hello</code>.
   2) If message <code>Hello World!</code> is received, the server is started correctly.
2) In browser
   1) Type <code>http://localhost:9000/hello</code> in browser.
   2) If index page is loaded, server is started correctly.