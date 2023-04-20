from flask import Flask, make_response, g, request, send_file
import logging
from utils import is_raspberry_pi

# Instantiate the Flask app (must be before the endpoint functions)
app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    print("Hello!")
    print("this runs locally")
    return make_response({'message': 'Hello World!'}, 200)

@app.errorhandler(500)
def server_error(e):
    logging.exception("Internal error: %s", e)
    return make_response({"error": str(e)}, 500)

# Start the Flask app (must be after the endpoint functions) 
host_local_computer = "localhost" # Listen for connections on the local computer
host_local_network = "0.0.0.0" # Listen for connections on the local network
app.run(host=host_local_network if is_raspberry_pi() else host_local_computer, port=9000)
