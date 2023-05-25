from setuptools import setup, find_packages

setup(
    name='weather_station',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_mqtt',
        'flask_cors',
        'flask_socketio',
        'paho-mqtt',
    ],
)