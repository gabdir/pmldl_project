from tensorflow.keras.models import load_model
from tinder.decision_making.model import process_image
import numpy as np
from skimage import io
import cv2


def make_test_prediction(image_path):
    pic = io.imread(image_path, plugin='matplotlib')
    img = cv2.cvtColor(pic, cv2.COLOR_RGB2BGR)
    dim = (640, 640)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
    image = np.expand_dims(resized_img, axis=0)
    model = load_model('cnn_model.h5')
    prediction = model.predict(image)
    print(prediction)