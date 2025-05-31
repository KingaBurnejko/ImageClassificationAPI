import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras import backend as K
import json
from dotenv import load_dotenv
import os

load_dotenv()

IMG_SIZE = (int(os.getenv("IMG_HEIGHT")), int(os.getenv("IMG_WIDTH")))
MODEL_PATH = os.getenv("MODEL_PATH")
LABELS_PATH = os.getenv("LABELS_PATH")

def F1_score(y_true, y_pred):
    y_pred = tf.round(y_pred)
    tp = tf.reduce_sum(tf.cast(y_true * y_pred, 'float'), axis=0)
    predicted_positives = tf.reduce_sum(tf.cast(y_pred, 'float'), axis=0)
    actual_positives = tf.reduce_sum(tf.cast(y_true, 'float'), axis=0)

    precision = tp / (predicted_positives + K.epsilon())
    recall = tp / (actual_positives + K.epsilon())
    f1 = 2 * precision * recall / (precision + recall + K.epsilon())
    return tf.reduce_mean(f1)

def load_model_and_labels():
    model = tf.keras.models.load_model(
        MODEL_PATH,
        custom_objects={"F1_score": F1_score}
    )
    with open(LABELS_PATH, "r") as f:
        class_names = json.load(f)
    return model, class_names

def preprocess_image(img):
    img = img.resize(IMG_SIZE)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    return preprocess_input(img_array)
