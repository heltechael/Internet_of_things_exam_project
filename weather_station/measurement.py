from datetime import datetime
from random import randrange
from sense_hat import SenseHat

sense = SenseHat()

class Measurement:
    def __init__(self, sensor_id: str, value: float = None, timestamp: datetime = None):
        self.sensor_id = sensor_id

        if value is not None:
            self.value = value
        else:
            if sensor_id == 'temperature':
                self.value = sense.get_temperature()
            elif sensor_id == 'humidity':
                self.value = sense.get_humidity()
            elif sensor_id == 'pressure':
                self.value = sense.get_pressure()
            else:
                # Handle the case when sensor_id does not match any known sensor
                self.value = None  # or assign a default value or raise an exception

        self.timestamp = timestamp if timestamp else datetime.utcnow()

    def to_dict(self):
        return {
            'sensor_id': self.sensor_id,
            'value': self.value,
            'timestamp': self.timestamp.isoformat(), # Convert datetime object to string in ISO format
        }
    
    @staticmethod
    def from_dict(data):
        return Measurement(
            sensor_id=data['sensor_id'],
            value=data['value'],
            timestamp=datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else None
        )
