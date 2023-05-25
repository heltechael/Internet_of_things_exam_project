from analytics import Analytics

analytics = Analytics('database2.db')

print(analytics.get_all_rows(print_results=True))
print("max temp: ", analytics.get_max('temperature'))
print("min temp: ", analytics.get_min('pressure'))
print("max temp: ", analytics.get_max('temperature',return_timestamp=True))
print("min temp: ", analytics.get_min('pressure',return_timestamp=True))
print("get_sensor_count temp: ", analytics.get_sensor_count('temperature'))
print("get_time_range temp: ", analytics.get_time_range('temperature'))
