import paho.mqtt.client as mqtt
import base64
import json
import os
from ai_processor import ImageClassifier
from annotate import Annotate

with open("config.json", "r") as f:
    config = json.load(f)

annotate = Annotate(config=config)

classifier = ImageClassifier(
    model_path='model.tflite',
    labelmap_path='labelmap.txt',
    threshold=0.7,
    top_k=3
)

MQTT_BROKER = config["mqtt"]["broker"]
MQTT_PORT = config["mqtt"]["port"]
MQTT_USER = config["mqtt"]["username"]
MQTT_PASS = config["mqtt"]["password"]
TOPIC_GLOBAL = config["mqtt"]["topics"]["globalCommand"]
TOPIC_RESPONSE = config["mqtt"]["topics"]["response"]
SAVE_PATH = config["savePath"]

os.makedirs(SAVE_PATH, exist_ok=True)

# -- Listeners --
def on_connect(client, userdata, flags, rc, properties):
    print(f"Server connected (RC: {rc})")
    client.subscribe(TOPIC_RESPONSE, qos=1)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        filename = f"{SAVE_PATH}/{payload['cameraId']}_{payload['timestamp']}.jpg"
        
        with open(filename, "wb") as f:
            f.write(base64.b64decode(payload["image"]))
        
        print(f"Saved {filename}")
        try:
            img, draw = annotate.open_image(filename=filename)

            classification_result = classifier.classify_image(filename)
            if classification_result[0]:
                annotate.annotate_classification(draw, 
                                                classification_name=classification_result[0][0]["label"], 
                                                classification_percentage=classification_result[0][0]["confidence"])
            else:
                annotate.annotate_classification(draw, 
                                                classification_name="None", 
                                                classification_percentage="0.00")
            annotate.annotate_id(draw, payload['cameraId'])
            annotate.annotate_timestamp(draw)
            annotate.save_and_close_image(img)

        except Exception as e:
            print(f"Annotations failed: {str(e)}")
            
        return True

    except Exception as e:
        print(f"Error processing message: {str(e)}")

# -- Main --
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# command interface -- for testing, would need to make work with WebApp
while True:
    cmd = input("\nCommand:\n1. Global photo\n2. Personal photo\n> ")
    
    if cmd == "1":
        client.publish(TOPIC_GLOBAL, "capture", qos=1)
        print("Sent global command!")
    elif cmd == "2":
        camera_id = input("Camera ID: ").strip()
        # Publish to camera-specific command topic
        client.publish(
            f"cameras/{camera_id}/command",
            "capture",
            qos=1
        )
        print(f"Sent to {camera_id}!")
    else:
        print("Invalid command")