"""
model.py
--------
Model architecture, loading, and prediction logic for AgriDoctor AI.

Two modes, chosen automatically:

1. TRAINED MODE
   If models/agridoctor_model.h5 exists, it is loaded and used for real
   MobileNetV2-based predictions. Produce this file by running train_model.py
   against a labeled leaf-image dataset (see README.md).

2. DEMO MODE (fallback, no training required)
   If no trained model is found -- e.g. running the prototype for the first
   time, or on a machine without the PlantVillage dataset -- predictions
   come from `heuristic_predict()`. It looks at real colour statistics of
   the uploaded image (fraction of green vs. brown/yellow/dark pixels) to
   choose a plausible class and confidence, so the demo still responds
   differently to different photos instead of returning a hardcoded answer.
   The UI clearly labels this as Demo Mode -- it is a stand-in for judges
   and testers, never presented as a trained result.
"""

from pathlib import Path
import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "agridoctor_model.h5"
IMG_SIZE = (224, 224)

# Order MUST match the class indices produced by train_model.py
# (alphabetical order of the training subfolders under data/train/)
CLASS_NAMES = [
    "Corn_Common_Rust",
    "Corn_Gray_Leaf_Spot",
    "Corn_Healthy",
    "Potato_Early_Blight",
    "Potato_Healthy",
    "Potato_Late_Blight",
    "Tomato_Early_Blight",
    "Tomato_Healthy",
    "Tomato_Late_Blight",
    "Tomato_Leaf_Mold",
]


def build_model(num_classes: int = len(CLASS_NAMES), fine_tune: bool = False):
    """
    Build the MobileNetV2 transfer-learning architecture used for training.
    Only imports TensorFlow when actually called, so the rest of the app
    (demo mode) works even on machines where TensorFlow isn't installed yet.
    """
    import tensorflow as tf
    from tensorflow.keras import layers, models

    try:
        base = tf.keras.applications.MobileNetV2(
            input_shape=(*IMG_SIZE, 3), include_top=False, weights="imagenet"
        )
    except Exception as e:
        # No internet access to download ImageNet weights -> fall back to
        # random initialization so training/testing can still proceed.
        print(f"[model.py] Could not load ImageNet weights ({e}); using random init.")
        base = tf.keras.applications.MobileNetV2(
            input_shape=(*IMG_SIZE, 3), include_top=False, weights=None
        )

    base.trainable = fine_tune

    model = models.Sequential(
        [
            base,
            layers.GlobalAveragePooling2D(),
            layers.Dense(128, activation="relu"),
            layers.Dropout(0.3),
            layers.Dense(num_classes, activation="softmax"),
        ]
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4 if fine_tune else 1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


_model_cache = {"model": None, "checked": False}


def load_trained_model():
    """Load the trained .h5 model if present. Returns None in demo mode."""
    if _model_cache["checked"]:
        return _model_cache["model"]

    _model_cache["checked"] = True
    if MODEL_PATH.exists():
        try:
            import tensorflow as tf

            _model_cache["model"] = tf.keras.models.load_model(MODEL_PATH)
            print(f"[model.py] Loaded trained model from {MODEL_PATH}")
        except Exception as e:
            print(f"[model.py] Failed to load trained model ({e}); using demo mode.")
            _model_cache["model"] = None
    else:
        print("[model.py] No trained model found - running in demo mode.")
        _model_cache["model"] = None

    return _model_cache["model"]


def preprocess_image(pil_image: Image.Image) -> np.ndarray:
    """Resize + scale an image the way the trained model expects."""
    img = pil_image.convert("RGB").resize(IMG_SIZE)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


# Per-crop disease options for demo mode, grouped by rough severity so the
# heuristic below only ever returns a class that actually belongs to the
# crop the user selected in the UI.
CROP_CLASSES = {
    "Tomato": {
        "healthy": "Tomato_Healthy",
        "mild": ["Tomato_Early_Blight", "Tomato_Leaf_Mold"],
        "severe": ["Tomato_Late_Blight"],
    },
    "Potato": {
        "healthy": "Potato_Healthy",
        "mild": ["Potato_Early_Blight"],
        "severe": ["Potato_Late_Blight"],
    },
    "Corn": {
        "healthy": "Corn_Healthy",
        "mild": ["Corn_Common_Rust"],
        "severe": ["Corn_Gray_Leaf_Spot"],
    },
}


def _image_variety_index(arr: np.ndarray, n: int) -> int:
    """Stable per-image index (0..n-1) so different photos in the same
    severity bucket don't all collapse onto the same disease."""
    if n <= 1:
        return 0
    fingerprint = float(np.sum(arr * np.arange(arr.size).reshape(arr.shape) % 97))
    return int(abs(fingerprint)) % n


def heuristic_predict(pil_image: Image.Image, crop: str = None):
    """
    Offline, dependency-free stand-in for a trained model. Uses real pixel
    statistics from the image so different photos genuinely give different
    results -- deterministic, explainable, and clearly not a trained model.

    `crop` should be one of CROP_CLASSES' keys ("Tomato", "Potato", "Corn").
    If given, only that crop's classes are ever returned -- e.g. picking
    "Corn" in the UI will never come back as a Tomato result.
    """
    img = pil_image.convert("RGB").resize((128, 128))
    arr_full = np.asarray(img, dtype=np.float32) / 255.0

    # Focus on the leaf, not the whole photo. Real photos usually have a
    # plain background (white/gray studio background, or a hand/soil around
    # the leaf), which was swamping the colour stats below. We approximate
    # "leaf pixels" as: not near-white/near-black background, restricted to
    # a centre crop (leaves are usually roughly centred in the frame).
    h, w, _ = arr_full.shape
    m = int(h * 0.15)
    arr = arr_full[m:h - m, m:w - m, :]

    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    brightness = (r + g + b) / 3

    bg_mask = (brightness > 0.85) | (brightness < 0.06)  # near-white / near-black backdrop
    leaf_mask = ~bg_mask
    if leaf_mask.sum() < 0.05 * leaf_mask.size:
        # Almost nothing left after removing "background" -> the whole
        # image is probably leaf already; fall back to using all of it.
        leaf_mask = np.ones_like(leaf_mask)

    def frac(mask):
        combined = mask & leaf_mask
        denom = leaf_mask.sum()
        return float(combined.sum()) / float(denom) if denom > 0 else 0.0

    green_frac = frac((g > r) & (g > b))
    brown_frac = frac((r > 0.30) & (g > 0.15) & (b < 0.40) & (r >= b))
    dark_frac = frac(brightness < 0.28)

    crop_key = crop if crop in CROP_CLASSES else None
    classes = CROP_CLASSES.get(crop_key, CROP_CLASSES["Tomato"])

    # Decide by which colour clearly dominates the leaf pixels, rather than
    # small absolute thresholds -- a lot more forgiving of shadows, uneven
    # lighting, and backgrounds in real photos.
    if green_frac >= brown_frac and green_frac >= dark_frac and green_frac > 0.35:
        class_name = classes["healthy"]
        confidence = min(0.97, 0.80 + green_frac * 0.2)
    elif dark_frac > green_frac and dark_frac > brown_frac:
        pool = classes["severe"] or classes["mild"]
        idx = _image_variety_index(arr, len(pool))
        class_name = pool[idx]
        confidence = min(0.95, 0.72 + dark_frac * 0.5)
    else:
        # Default / ambiguous case -> mild bucket, not severe. Most
        # real-world photos (varied lighting, backgrounds) land here.
        pool = classes["mild"] or classes["severe"]
        idx = _image_variety_index(arr, len(pool))
        class_name = pool[idx]
        confidence = min(0.92, 0.65 + brown_frac * 1.0)

    return class_name, round(float(confidence), 4)


def predict(pil_image: Image.Image, crop: str = None):
    """
    Main entry point used by app.py.
    `crop` (e.g. "Tomato"/"Potato"/"Corn") is used in demo mode to keep
    results specific to the selected crop; a trained model ignores it and
    classifies across all classes directly.
    Returns (class_name, confidence, mode) where mode is "trained" or "demo".
    """
    model = load_trained_model()

    if model is not None:
        batch = preprocess_image(pil_image)
        preds = model.predict(batch, verbose=0)[0]
        idx = int(np.argmax(preds))
        return CLASS_NAMES[idx], round(float(preds[idx]), 4), "trained"

    class_name, confidence = heuristic_predict(pil_image, crop=crop)
    return class_name, confidence, "demo"


if __name__ == "__main__":
    # Quick manual smoke test with a synthetic green square image.
    test_img = Image.new("RGB", (224, 224), color=(60, 140, 60))
    result = predict(test_img)
    print("Prediction on synthetic green image:", result)
