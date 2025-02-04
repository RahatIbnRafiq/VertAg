from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class Annotate:
    def __init__(self, config):
        self.config = config
        self.new_filename = None

    def open_image(self, filename):
        img = Image.open(filename)
        draw = ImageDraw.Draw(img)
        self.new_filename = filename.replace(".jpg", "_annotated.jpg")

        return img, draw
    
    def save_and_close_image(self, img):
        img.save(self.new_filename)
        print("Annotations added!")

    def annotate_id(self, draw, camera_id):
        ID_FONT_SIZE = self.config["idText"]["fontSize"]
        ID_FONT_COLOR = tuple(self.config["idText"]["fontColor"])
        ID_POSITION = tuple(self.config["idText"]["position"])

        # Load font (use default if path not specified)
        ID_FONT_PATH = self.config["idText"].get("fontPath", None)
        if ID_FONT_PATH and os.path.exists(ID_FONT_PATH):
            ID_FONT = ImageFont.truetype(ID_FONT_PATH, ID_FONT_SIZE)
        else:
            ID_FONT = ImageFont.load_default()
        

        id = camera_id.upper()
        draw.text(ID_POSITION, id, font=ID_FONT, fill=ID_FONT_COLOR)
        return
    
    def annotate_timestamp(self, draw):
        TIMESTAMP_FONT_SIZE = self.config["timestampText"]["fontSize"]
        TIMESTAMP_FONT_COLOR = tuple(self.config["timestampText"]["fontColor"])  # RGB tuple
        TIMESTAMP_POSITION = tuple(self.config["timestampText"]["position"])     # (x, y)

        # Load font (use default if path not specified)
        TIMESTAMP_FONT_PATH = self.config["timestampText"].get("fontPath", None)
        if TIMESTAMP_FONT_PATH and os.path.exists(TIMESTAMP_FONT_PATH):
            TIMESTAMP_FONT = ImageFont.truetype(TIMESTAMP_FONT_PATH, TIMESTAMP_FONT_SIZE)
        else:
            TIMESTAMP_FONT = ImageFont.load_default()

        timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        draw.text(TIMESTAMP_POSITION, timestamp, font=TIMESTAMP_FONT, fill=TIMESTAMP_FONT_COLOR)
        return
    
    def annotate_classification(self, draw, classification_name, classification_percentage):
        CLASSIFICATION_FONT_SIZE = self.config["classificationText"]["fontSize"]
        CLASSIFICATION_FONT_COLOR = tuple(self.config['classificationText']["fontColor"])
        CLASSIFICATION_POSITION = tuple(self.config["classificationText"]["position"])

        # Load font (use default if path not specified)
        CLASSIFICATION_FONT_PATH = self.config["classificationText"].get("fontPath", None)
        if CLASSIFICATION_FONT_PATH and os.path.exists(CLASSIFICATION_FONT_PATH):
            CLASSIFICATION_FONT = ImageFont.truetype(CLASSIFICATION_FONT_PATH, CLASSIFICATION_FONT_SIZE)
        else:
            CLASSIFICATION_FONT = ImageFont.load_default()

        classification = f'{classification_name.upper()}: {classification_percentage*100:.2f}%'
        draw.text(CLASSIFICATION_POSITION, classification, font=CLASSIFICATION_FONT, fill=CLASSIFICATION_FONT_COLOR)
        return