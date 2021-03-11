import cv2
import numpy as np
from skimage import io
from tensorflow.keras.models import load_model


class Model:
    IMG_SIZE = 224

    def __init__(self, model_path):
        self.model = load_model(model_path)

    @staticmethod
    def process_external_image(image_url):
        img = io.imread(image_url, plugin='matplotlib')
        dim = (Model.IMG_SIZE, Model.IMG_SIZE)
        resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
        image = np.expand_dims(resized_img, axis=0)
        return image

    def predict(self, img_url):
        image = self.process_external_image(img_url)
        prediction = self.model.predict(image)
        return round(prediction[0][0])
