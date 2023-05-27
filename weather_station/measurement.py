from datetime import datetime
from random import randrange
#from sense_hat import SenseHat

#sense = SenseHat()

class Measurement:
    def __init__(self, sensor_id: str, value: float = None, timestamp: datetime = None):
        self.sensor_id = sensor_id

        if value is not None:
            self.value = value
        else:
            match sensor_id:
                case 'temperature':
                    self.value = sense.get_temperature()
                case 'humidity':
                    self.value = sense.get_humidity()
                case 'pressure':
                    self.value = sense.get_pressure()

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
