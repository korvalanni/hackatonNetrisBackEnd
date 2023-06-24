import io
from os.path import exists
from config import CATEGORIES, IMAGE_DIM, MODEL_PATH

import numpy as np
import requests
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image


def load_images(uri, image_size):
    loaded_images = []

    try:
        response = requests.get(uri)
        with io.BytesIO(response.content) as img_bytes:
            image = Image.open(img_bytes)
            image = image.resize(image_size, Image.NEAREST)
        image = tf.keras.preprocessing.image.img_to_array(image)

        image /= 255
        loaded_images.append(image)
    except Exception as ex:
        print("Image Load Failure: ", uri, ex)

    return np.asarray(loaded_images)


def load_model(model_path):
    if model_path is None or not exists(model_path):
        raise ValueError("Bad model path")
    return tf.keras.models.load_model(model_path,
                                      custom_objects={'KerasLayer': hub.KerasLayer})


def classify(uri, image_dim=IMAGE_DIM):
    images = load_images(uri, (image_dim, image_dim))
    model_preds = model.predict(images)
    for single_preds in model_preds:
        return {CATEGORIES[idx]: float(rel) for idx, rel in enumerate(single_preds)}


model = load_model(MODEL_PATH)
