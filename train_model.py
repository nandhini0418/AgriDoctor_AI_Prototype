"""
train_model.py
---------------
Trains the real AgriDoctor AI disease classifier using transfer learning on
MobileNetV2. Run this once you have a labeled leaf-image dataset -- for
example the PlantVillage dataset (https://www.kaggle.com/datasets/emmarex/plantdisease).

Expected folder layout:

    data/
      train/
        Tomato_Healthy/          *.jpg
        Tomato_Early_Blight/     *.jpg
        Potato_Late_Blight/      *.jpg
        ... one subfolder per class in model.CLASS_NAMES ...
      val/
        Tomato_Healthy/
        ...

Usage:
    python train_model.py --data_dir data --epochs 15 --batch_size 32

Output:
    models/agridoctor_model.h5   (loaded automatically by model.py / app.py)
"""

import argparse
from pathlib import Path

from model import build_model, IMG_SIZE, CLASS_NAMES


def main():
    parser = argparse.ArgumentParser(description="Train the AgriDoctor AI classifier.")
    parser.add_argument("--data_dir", type=str, default="data", help="Folder containing train/ and val/ subfolders")
    parser.add_argument("--epochs", type=int, default=15, help="Epochs for the initial (frozen-base) phase")
    parser.add_argument("--fine_tune_epochs", type=int, default=5, help="Extra epochs with the base unfrozen")
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--output", type=str, default="models/agridoctor_model.h5")
    args = parser.parse_args()

    import tensorflow as tf

    data_dir = Path(args.data_dir)
    train_dir = data_dir / "train"
    val_dir = data_dir / "val"

    if not train_dir.exists():
        raise SystemExit(
            f"Could not find {train_dir}. Create data/train/<class_name>/ folders "
            f"with labeled images first -- see the docstring at the top of this file."
        )

    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir, image_size=IMG_SIZE, batch_size=args.batch_size, label_mode="categorical"
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        val_dir if val_dir.exists() else train_dir,
        image_size=IMG_SIZE,
        batch_size=args.batch_size,
        label_mode="categorical",
    )

    found_classes = train_ds.class_names
    if found_classes != CLASS_NAMES:
        print("WARNING: classes found on disk do not match model.CLASS_NAMES.")
        print("  On disk:        ", found_classes)
        print("  model.CLASS_NAMES:", CLASS_NAMES)
        print("  Update CLASS_NAMES in model.py to match, or rename your folders, "
              "otherwise predictions will be mislabeled.")

    normalize = tf.keras.layers.Rescaling(1.0 / 255)
    train_ds = train_ds.map(lambda x, y: (normalize(x), y)).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.map(lambda x, y: (normalize(x), y)).prefetch(tf.data.AUTOTUNE)

    print(f"Training on {len(found_classes)} classes: {found_classes}")

    # Phase 1: train the classification head with the MobileNetV2 base frozen.
    model = build_model(num_classes=len(found_classes), fine_tune=False)
    model.fit(train_ds, validation_data=val_ds, epochs=args.epochs)

    # Phase 2: unfreeze the base for a few epochs of fine-tuning at a lower LR.
    if args.fine_tune_epochs > 0:
        print("Fine-tuning base model...")
        model.layers[0].trainable = True
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )
        model.fit(train_ds, validation_data=val_ds, epochs=args.fine_tune_epochs)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(out_path)
    print(f"Saved trained model to {out_path}")


if __name__ == "__main__":
    main()
