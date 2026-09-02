from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "ecosort.keras"
CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"
HISTORY_PATH = MODEL_DIR / "history.json"
METRICS_PATH = MODEL_DIR / "metrics.json"
CONFUSION_MATRIX_PATH = MODEL_DIR / "confusion_matrix.png"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

CLASS_NAMES = [
    "Aluminium",
    "Carton",
    "E-waste",
    "Glass",
    "Organic_Waste",
    "Paper_and_Cardboard",
    "Plastics",
    "Textiles",
    "Wood",
]

MODEL_DIR.mkdir(parents=True, exist_ok=True)