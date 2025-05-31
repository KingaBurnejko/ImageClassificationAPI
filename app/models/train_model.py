import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image_dataset_from_directory
from app.models.dataset_utils import generate_labels_csv
from app.models.model_utils import F1_score
from dotenv import load_dotenv
load_dotenv()

IMG_SIZE = (int(os.getenv("IMG_HEIGHT")), int(os.getenv("IMG_WIDTH")))
BATCH_SIZE = int(os.getenv("BATCH_SIZE"))
DATA_DIR = os.getenv("DATA_DIR")
MODEL_PATH = os.getenv("MODEL_PATH")
EPOCHS = int(os.getenv("EPOCHS"))
LABELS_PATH = os.getenv("LABELS_PATH")
STATUS_PATH = os.getenv("STATUS_PATH")

def update_status(status, error=None):
    with open(STATUS_PATH, "w") as f:
        json.dump({"status": status, "error": error}, f)

def train_model():
    generate_labels_csv(os.path.join(DATA_DIR, "train"))
    try:
        update_status("in_progress")

        train_ds = image_dataset_from_directory(
            os.path.join(DATA_DIR, "train"),
            image_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            label_mode="categorical"
        )

        val_ds = image_dataset_from_directory(
            os.path.join(DATA_DIR, "valid"),
            image_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            label_mode="categorical"
        )

        class_names = train_ds.class_names
        num_classes = len(class_names)

        with open(LABELS_PATH, "w") as f:
            json.dump(class_names, f)

        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        base_model.trainable = False

        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(128, activation='relu'),
            layers.Dense(num_classes, activation='softmax')
        ])

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy', F1_score])

        model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)
        model.save(MODEL_PATH)

        update_status("done")
        return {"status": "Model trained and saved", "classes": class_names}

    except Exception as e:
        update_status("error", str(e))
        raise e
