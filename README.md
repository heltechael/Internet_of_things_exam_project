# Weather Station Project

Exam project for Internet of Things course at AU 2023.

Members:
- Anisa Nuur
- Dilan Celebi
- Michael Nørbo

## Installation
1) Install dependencies with <code>pip install -r requirements</code>.
2) Install eventlet

## Running 
1) Open terminal and start mosquitto: </code>mosquitto -p 9001</code>.
2) Open new terminal and start server: <code>python server.py</code>.
3) Open new terminal and connect nodes: <code>python node.py</code>.

## Making sure everything works locally
1) In terminal
   1) Type <code>curl http://localhost:9000/hello</code>.
   2) If message <code>Hello World!</code> is received, the server is started correctly.
2) In browser
   1) Type <code>http://localhost:9000/hello</code> in browser.
   2) If index page is loaded, server is started correctly.