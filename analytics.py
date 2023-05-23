import sqlite3
import statistics

class Analytics:

    def __init__(self, db_name):
        self.db_name = db_name

    def _get_values_for_sensor(self, sensor_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM measurements WHERE sensor_id=?", (sensor_id,))
            values = [row[0] for row in cursor.fetchall()]
            return values

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def get_max(self, sensor_id, return_timestamp=False):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(f"SELECT value, timestamp FROM measurements WHERE sensor_id=? ORDER BY value DESC", (sensor_id,))
        result = c.fetchone()
        conn.close()
        if result:
            return (result[0], result[1]) if return_timestamp else result[0] 
        else:
            print(f"No measurements for {sensor_id} found in database.")
            return None

    def get_min(self, sensor_id, return_timestamp=False):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(f"SELECT value, timestamp FROM measurements WHERE sensor_id=? ORDER BY value", (sensor_id,))
        result = c.fetchone()
        conn.close()
        if result:
            return (result[0], result[1]) if return_timestamp else result[0] 
        else:
            print(f"No measurements for {sensor_id} found in database.")
            return None

    def get_avg(self, sensor_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(f"SELECT AVG(value) FROM measurements WHERE sensor_id=?", (sensor_id,))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0] 
        else:
            print(f"No measurements for {sensor_id} found in database.")
            return None
    
    def get_median(self, sensor_id):
        values = self._get_values_for_sensor(sensor_id)
        return statistics.median(values)

    def get_mode(self, sensor_id):
        values = self._get_values_for_sensor(sensor_id)
        return statistics.mode(values)

    def get_sensor_count(self, sensor_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM measurements WHERE sensor_id=?", (sensor_id,))
            count = cursor.fetchone()[0]
            return count

    def get_time_range(self, sensor_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM measurements WHERE sensor_id=?", (sensor_id,))
            start, end = cursor.fetchone()
            return start, end
        
    def get_all_rows(self, print_results=False):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM measurements")
        results = c.fetchall()
        conn.close()

        if print_results:
            for row in results:
                print(row)
        else:
            if not results:
                print("No measurements found in database.")
            else:
                return results
        
     