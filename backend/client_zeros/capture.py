import paho.mqtt.client as mqtt
import subprocess
import base64
import time
import json
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

with open("config.json", "r") as f:
    config = json.load(f)

CAMERA_ID = config["cameraId"]
MQTT_BROKER = config["mqtt"]["broker"]
MQTT_PORT = config["mqtt"]["port"]
MQTT_USER = config["mqtt"]["username"]
MQTT_PASS = config["mqtt"]["password"]
TOPIC_PERSONAL = config["mqtt"]["topics"]["personalCommand"]
TOPIC_GLOBAL = config["mqtt"]["topics"]["globalCommand"]
TOPIC_RESPONSE = config["mqtt"]["topics"]["response"]
TOPIC_ERROR = config["mqtt"]["topics"]["error"]

# camera settings
CAM_RESOLUTION = (config["cameraSettings"]["resolution"]["width"], 
                  config["cameraSettings"]["resolution"]["height"])
CAM_TIMEOUT = config["cameraSettings"]["timeout"]

# -- photo logic --
def take_and_send_photo(client):
    try:
        timestamp = int(time.time())
        image_path = f"/tmp/photo_{CAMERA_ID}_{timestamp}.jpg"

        # capture
        result = subprocess.run(
            [
                "libcamera-jpeg",
                "-o", image_path,
                "--width", str(CAM_RESOLUTION[0]),
                "--height", str(CAM_RESOLUTION[1]),
                "--timeout", str(CAM_TIMEOUT * 1000)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"Camera error: {result.stderr}")

        # read and encode image
        with open(image_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode("utf-8")

        # publish the payload
        payload = {
            "cameraId": CAMERA_ID,
            "timestamp": timestamp,
            "image": encoded_image
        }
        client.publish(TOPIC_RESPONSE, json.dumps(payload), qos=1)
        print(f"Photo sent from {CAMERA_ID}!")
        os.remove(image_path)

    except Exception as e:
        print(f"Error: {str(e)}")
        client.publish(TOPIC_ERROR, json.dumps({
            "cameraId": CAMERA_ID,
            "error": str(e)
        }))

# -- Listeners --
def on_connect(client, userdata, flags, rc, properties):
    print(f"Connected to MQTT Broker (RC: {rc})")
    client.subscribe([
        (TOPIC_GLOBAL, 1),
        (TOPIC_PERSONAL, 1)
    ])

def on_message(client, userdata, msg):
    if msg.topic == TOPIC_GLOBAL:
        print("Global command received!")
        take_and_send_photo(client)
    elif msg.topic.startswith("cameras/"):
        # Extract camera ID from topic
        _, camera_id, _ = msg.topic.split('/')
        if camera_id == CAMERA_ID:
            print(f"Personal command for {CAMERA_ID} received!")
            take_and_send_photo(client)

# -- Main --
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 120)
client.loop_forever()