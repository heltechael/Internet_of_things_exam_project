from datetime import datetime
import pandas as pd

class Latency:
    def __init__(self):
        self.latencies = {"sensor_id": [], "latency": []}
        self.count = 0

    def convert_timestamp(self, timestamp):
        if type(timestamp) is str:
            return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        else:
            return timestamp

    def add_measurement(self, sensor_id, server_timestamp, node_timestamp):
        # Compute the latency and append it to the list
        latency = self.convert_timestamp(server_timestamp) - self.convert_timestamp(node_timestamp)
        self.latencies["sensor_id"].append(sensor_id)
        self.latencies["latency"].append(latency.total_seconds())
        self.count += 1

    def get_latencies(self):
        return self.latencies
    
    def get_count(self):
        return self.count
    
    def save_csv(self):
        df = pd.DataFrame(self.latencies) 
        df.to_csv('latencies.csv')