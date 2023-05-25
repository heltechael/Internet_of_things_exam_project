from datetime import datetime

class Measurement:
    def __init__(self, sensor_id: str, value: float, timestamp: datetime = None):
        self.sensor_id = sensor_id
        self.value = value
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
            sensor_id = data['sensor_id'],
            value = data['value'],
            timestamp = datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else None
        )
