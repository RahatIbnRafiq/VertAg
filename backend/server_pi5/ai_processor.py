import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter

class ImageClassifier:
    def __init__(self, model_path='model.tflite', labelmap_path='labelmap.txt', 
                 threshold=0.7, top_k=3):
        
        self.interpreter = Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # model parameters
        self.input_shape = self.input_details[0]['shape'][1:3]  # (height, width)
        self.threshold = threshold
        self.top_k = top_k
        
        with open(labelmap_path, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

    def preprocess_image(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            return None, None
            
        # convert to RGB + resize
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (self.input_shape[1], self.input_shape[0]))
        
        # normalize
        input_data = np.expand_dims(img_resized.astype(np.float32) / 255.0, axis=0)
        return input_data, img

    def classify_image(self, image_path):
        # preprocess image
        input_data, original_img = self.preprocess_image(image_path)
        if input_data is None:
            return None

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        predictions = output_data[0]  # Remove batch dimension
        
        # get top predictions
        top_k_indices = np.argsort(predictions)[-self.top_k:][::-1]
        results = []
        
        for idx in top_k_indices:
            confidence = predictions[idx]
            if confidence < self.threshold:
                continue
            results.append({
                'label': self.labels[idx],
                'confidence': float(confidence)
            })
        
        return results, original_img