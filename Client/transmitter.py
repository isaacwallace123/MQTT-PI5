import paho.mqtt.client as paho

import adafruit_dht
import board
import time

dht_sensor = adafruit_dht.DHT11(board.D3)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = paho.Client()

client.on_connect = on_connect

if client.connect("localhost", 1883, 60) != 0:
    print("Couldn't connect to the mqtt broker")
    sys.exit(1)

while True:
    try:
        temp = dht_sensor.temperature
        humidity = dht_sensor.humidity

        print(f"Temperature: {temp}*C, Humidity: {humidity}%")
        client.publish("sensor/temphum", f"{temp},{humidity}", 0)
    except RuntimeError as error:
        print(f"Error reading DHT sensor: {error}")
    finally:
        time.sleep(0.5)

client.disconnect()