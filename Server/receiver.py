from flask import Flask, render_template, jsonify
import paho.mqtt.client as paho  # Imported as paho

sensor_data = {"temperature": [], "humidity": []}

# Broker

def on_connect(client, userdata, flags, rc):
    client.subscribe("sensor/temphum")

def on_message(client, userdata, msg):
    data = msg.payload.decode().split(',')

    temperature, humidity = float(data[0]), float(data[1])

    sensor_data["temperature"].append(temperature)
    sensor_data["humidity"].append(humidity)

client = paho.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.2", 1883, 60)

client.loop_start()

# Web Service

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor-data')
def get_sensor_data():
    return jsonify(sensor_data)

@app.route('/live-data')
def get_sensor_data_live():
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')