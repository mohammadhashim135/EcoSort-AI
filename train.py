import json
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

from config import (
    BATCH_SIZE,
    CLASS_NAMES,
    CLASS_NAMES_PATH,
    CONFUSION_MATRIX_PATH,
    DATA_DIR,
    HISTORY_PATH,
    IMAGE_SIZE,
    METRICS_PATH,
    MODEL_DIR,
    MODEL_PATH,
    SEED,
)

INITIAL_EPOCHS = 8
FINE_TUNE_EPOCHS = 12
VALIDATION_SPLIT = 0.2

tf.keras.utils.set_random_seed(SEED)

MODEL_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_DIR.exists():
    raise FileNotFoundError(f"Dataset directory not found: {DATA_DIR}")

print("EcoSort AI training started")
print(f"Dataset: {DATA_DIR}")
print(f"Image size: {IMAGE_SIZE}")
print(f"Batch size: {BATCH_SIZE}")
print(f"Initial epochs: {INITIAL_EPOCHS}")
print(f"Fine-tuning epochs: {FINE_TUNE_EPOCHS}")

file_paths = []
labels = []

valid_extensions = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
}

for class_index, class_name in enumerate(CLASS_NAMES):
    class_dir = DATA_DIR / class_name

    if not class_dir.exists():
        raise FileNotFoundError(f"Class directory not found: {class_dir}")

    for file_path in class_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
            file_paths.append(str(file_path))
            labels.append(class_index)

file_paths = np.array(file_paths)
labels = np.array(labels)

print(f"\nTotal images: {len(file_paths)}")

train_paths, validation_paths, train_labels, validation_labels = train_test_split(
    file_paths,
    labels,
    test_size=VALIDATION_SPLIT,
    random_state=SEED,
    stratify=labels,
)

print(f"Training images: {len(train_paths)}")
print(f"Validation images: {len(validation_paths)}")

print("\nTraining distribution:")

for index, class_name in enumerate(CLASS_NAMES):
    count = np.sum(train_labels == index)
    print(f"{class_name}: {count}")

print("\nValidation distribution:")

for index, class_name in enumerate(CLASS_NAMES):
    count = np.sum(validation_labels == index)
    print(f"{class_name}: {count}")

with open(CLASS_NAMES_PATH, "w", encoding="utf-8") as file:
    json.dump(CLASS_NAMES, file, indent=4)


def load_image(file_path, label):
    image = tf.io.read_file(file_path)
    image = tf.io.decode_image(
        image,
        channels=3,
        expand_animations=False,
    )
    image.set_shape([None, None, 3])
    image = tf.image.resize(image, IMAGE_SIZE)
    image = tf.cast(image, tf.float32)
    return image, label


train_dataset = tf.data.Dataset.from_tensor_slices(
    (train_paths, train_labels)
)

validation_dataset = tf.data.Dataset.from_tensor_slices(
    (validation_paths, validation_labels)
)

train_dataset = (
    train_dataset
    .shuffle(
        len(train_paths),
        seed=SEED,
        reshuffle_each_iteration=True,
    )
    .map(
        load_image,
        num_parallel_calls=tf.data.AUTOTUNE,
    )
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)

validation_dataset = (
    validation_dataset
    .map(
        load_image,
        num_parallel_calls=tf.data.AUTOTUNE,
    )
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)

data_augmentation = tf.keras.Sequential(
    [
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.08),
        tf.keras.layers.RandomZoom(0.1),
        tf.keras.layers.RandomContrast(0.1),
    ],
    name="data_augmentation",
)

base_model = tf.keras.applications.EfficientNetB0(
    include_top=False,
    weights="imagenet",
    input_shape=(
        IMAGE_SIZE[0],
        IMAGE_SIZE[1],
        3,
    ),
)

base_model.trainable = False

inputs = tf.keras.Input(
    shape=(
        IMAGE_SIZE[0],
        IMAGE_SIZE[1],
        3,
    )
)

x = data_augmentation(inputs)
x = base_model(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Dropout(0.3)(x)

outputs = tf.keras.layers.Dense(
    len(CLASS_NAMES),
    activation="softmax",
)(x)

model = tf.keras.Model(
    inputs,
    outputs,
    name="EcoSort_EfficientNetB0",
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001,
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

model.summary()

initial_callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        MODEL_PATH,
        monitor="val_accuracy",
        mode="max",
        save_best_only=True,
        verbose=1,
    ),
    tf.keras.callbacks.EarlyStopping(
        monitor="val_accuracy",
        mode="max",
        patience=3,
        restore_best_weights=True,
        verbose=1,
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        mode="min",
        factor=0.3,
        patience=2,
        min_lr=1e-6,
        verbose=1,
    ),
]

print("\nPhase 1: Training classification head")

history_initial = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=INITIAL_EPOCHS,
    callbacks=initial_callbacks,
)

base_model.trainable = True

fine_tune_from = int(len(base_model.layers) * 0.7)

for layer in base_model.layers[:fine_tune_from]:
    layer.trainable = False

for layer in base_model.layers[fine_tune_from:]:
    layer.trainable = True

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-5,
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

fine_tune_callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        MODEL_PATH,
        monitor="val_accuracy",
        mode="max",
        save_best_only=True,
        verbose=1,
    ),
    tf.keras.callbacks.EarlyStopping(
        monitor="val_accuracy",
        mode="max",
        patience=4,
        restore_best_weights=True,
        verbose=1,
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        mode="min",
        factor=0.3,
        patience=2,
        min_lr=1e-7,
        verbose=1,
    ),
]

print("\nPhase 2: Fine-tuning EfficientNetB0")

history_fine = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    initial_epoch=len(history_initial.history["loss"]),
    epochs=INITIAL_EPOCHS + FINE_TUNE_EPOCHS,
    callbacks=fine_tune_callbacks,
)

history_dict = {}

for key in history_initial.history:
    history_dict[key] = list(history_initial.history[key])

for key in history_fine.history:
    if key in history_dict:
        history_dict[key].extend(history_fine.history[key])
    else:
        history_dict[key] = list(history_fine.history[key])

with open(HISTORY_PATH, "w", encoding="utf-8") as file:
    json.dump(
        {
            key: [float(value) for value in values]
            for key, values in history_dict.items()
        },
        file,
        indent=4,
    )

print("\nLoading best model")

model = tf.keras.models.load_model(MODEL_PATH)

print("\nEvaluating model")

y_true = []
y_pred = []

for images, labels_batch in validation_dataset:
    predictions = model.predict(images, verbose=0)
    predicted_classes = np.argmax(predictions, axis=1)

    y_true.extend(labels_batch.numpy())
    y_pred.extend(predicted_classes)

y_true = np.array(y_true)
y_pred = np.array(y_pred)

accuracy = accuracy_score(y_true, y_pred)

precision = precision_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0,
)

recall = recall_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0,
)

f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0,
)

metrics = {
    "accuracy": float(accuracy),
    "precision": float(precision),
    "recall": float(recall),
    "f1_score": float(f1),
}

with open(METRICS_PATH, "w", encoding="utf-8") as file:
    json.dump(metrics, file, indent=4)

report = classification_report(
    y_true,
    y_pred,
    labels=np.arange(len(CLASS_NAMES)),
    target_names=CLASS_NAMES,
    zero_division=0,
)

print("\nClassification Report")
print(report)

cm = confusion_matrix(
    y_true,
    y_pred,
    labels=np.arange(len(CLASS_NAMES)),
)

fig, ax = plt.subplots(figsize=(11, 9))

ax.imshow(cm)

ax.set_title("EcoSort AI - Confusion Matrix")
ax.set_xlabel("Predicted Class")
ax.set_ylabel("Actual Class")

ax.set_xticks(range(len(CLASS_NAMES)))
ax.set_yticks(range(len(CLASS_NAMES)))

ax.set_xticklabels(
    CLASS_NAMES,
    rotation=45,
    ha="right",
)

ax.set_yticklabels(CLASS_NAMES)

for i in range(len(CLASS_NAMES)):
    for j in range(len(CLASS_NAMES)):
        ax.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center",
        )

fig.tight_layout()

fig.savefig(
    CONFUSION_MATRIX_PATH,
    dpi=150,
    bbox_inches="tight",
)

plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(
    history_dict["accuracy"],
    label="Training Accuracy",
)

ax.plot(
    history_dict["val_accuracy"],
    label="Validation Accuracy",
)

ax.set_title("Training vs Validation Accuracy")
ax.set_xlabel("Epoch")
ax.set_ylabel("Accuracy")
ax.legend()

fig.tight_layout()

fig.savefig(
    MODEL_DIR / "accuracy.png",
    dpi=150,
    bbox_inches="tight",
)

plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(
    history_dict["loss"],
    label="Training Loss",
)

ax.plot(
    history_dict["val_loss"],
    label="Validation Loss",
)

ax.set_title("Training vs Validation Loss")
ax.set_xlabel("Epoch")
ax.set_ylabel("Loss")
ax.legend()

fig.tight_layout()

fig.savefig(
    MODEL_DIR / "loss.png",
    dpi=150,
    bbox_inches="tight",
)

plt.close(fig)

print("\n Alhamdullilah! Training completed successfully")

print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nSaved files:")
print(f"Model: {MODEL_PATH}")
print(f"Class names: {CLASS_NAMES_PATH}")
print(f"History: {HISTORY_PATH}")
print(f"Metrics: {METRICS_PATH}")
print(f"Confusion matrix: {CONFUSION_MATRIX_PATH}")