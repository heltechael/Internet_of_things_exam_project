import unittest
import sqlite3
from flask_testing import TestCase

## import
from ..server import Server
from ..measurement import Measurement

class ServerTest(TestCase):

    def create_app(self):
        self.server = Server()
        self.server.app.config['TESTING'] = True
        return self.server.app

    def setUp(self):
        self.server.init_db()

    def tearDown(self):
        self.server.close_connection(None)

    def test_db_insertion(self):
        measurement = Measurement("temperature", 25.0, "2023-05-24T14:30:00Z")
        with self.server.app.app_context():
            conn = self.server.get_db()
            c = conn.cursor()
            c.execute("INSERT INTO measurements (sensor_id, value, timestamp) VALUES (?, ?, ?)",
                    (measurement.sensor_id, measurement.value, measurement.timestamp))
            conn.commit()

            c.execute("SELECT * FROM measurements WHERE sensor_id = ?", (measurement.sensor_id,))
            result = c.fetchone()
            self.assertIsNotNone(result)

    def test_hello_endpoint(self):
        response = self.client.get('/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Hello World!'})

if __name__ == "__main__":
    unittest.main(verbosity=2) # verbosity=2 prints specific test results