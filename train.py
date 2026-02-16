# -*- coding: utf-8 -*-
import os

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam


def build_model(input_shape=(224, 224, 3)):
    base_model = MobileNetV2(include_top=False, input_shape=input_shape, weights="imagenet")
    base_model.trainable = False
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.2)(x)
    outputs = Dense(1, activation="sigmoid")(x)
    model = Model(inputs=base_model.input, outputs=outputs)
    model.compile(optimizer=Adam(learning_rate=1e-4), loss="binary_crossentropy", metrics=["accuracy"])
    return model


def get_data_generators(dataset_root: str, batch_size: int = 32):
    train_dir = os.path.join(dataset_root, "train")
    val_dir = os.path.join(dataset_root, "val")

    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=10,
        width_shift_range=0.05,
        height_shift_range=0.05,
        horizontal_flip=True,
    )
    val_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    # Ensure classes ordering maps: real -> 0, fake -> 1
    train_gen = train_datagen.flow_from_directory(
        train_dir,
        target_size=(224, 224),
        batch_size=batch_size,        class_mode="binary",
        classes=["real", "fake"],
    )
    val_gen = val_datagen.flow_from_directory(
        val_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode="binary",
        classes=["real", "fake"],
    )
    return train_gen, val_gen


if __name__ == "__main__":
    backend_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(backend_dir, os.pardir))
    dataset_root = os.path.join(project_root, "dataset")

    model = build_model()

    # If dataset folders are empty, training will fail. We guard and at least save an initial model.
    try:
        train_gen, val_gen = get_data_generators(dataset_root)
        epochs = int(os.environ.get("EPOCHS", "50"))
        steps_per_epoch = max(1, train_gen.samples // train_gen.batch_size)
        validation_steps = max(1, val_gen.samples // val_gen.batch_size)
        model.fit(train_gen, epochs=epochs, steps_per_epoch=steps_per_epoch, validation_data=val_gen, validation_steps=validation_steps)
    except Exception as e:
        print("[WARN] Training skipped due to an error (likely empty dataset):", e)
        print("[INFO] Saving initialized model without training so API can start.")

    save_path = os.path.join(backend_dir, "deepfake_model.h5")
    model.save(save_path)
    print(f"Model saved to: {save_path}")