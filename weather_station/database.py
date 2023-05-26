from flask import g
import sqlite3

class Database:
    def __init__(self, app):
        self.app = app

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect('database2.db')
        return db

    def close_connection(self, exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def init_db(self):
        with self.app.app_context():
            db = self.get_db()
            c = db.cursor()
            c.execute("DROP TABLE IF EXISTS measurements")
            with self.app.open_resource('schema.sql', mode='r') as f:
                c.executescript(f.read())
            db.commit()

    def insert_measurement(self, measurement):
        with self.app.app_context():
            conn = self.get_db()
            c = conn.cursor()
            c.execute("INSERT INTO measurements (sensor_id, value, timestamp) VALUES (?, ?, ?)",
                    (measurement.sensor_id, measurement.value, measurement.timestamp))
            conn.commit()
