# Training the Real AgriDoctor AI Model

This guide gets you from "demo mode" to a real trained classifier
(`models/agridoctor_model.h5`). It has two parts:

1. Get a labeled dataset organized into the exact folders `model.py` expects.
2. Run the training script — either on **Google Colab** (recommended) or
   on your own laptop.

## Why Colab is recommended

Training a CNN needs either a lot of patience (CPU: hours) or a GPU
(minutes). Google Colab gives you a **free GPU** and comes with TensorFlow
already installed — no repeating the local TensorFlow install you already
fought with. Unless you specifically want everything running locally,
use Colab for this one step, then download the trained file back to your
project folder.

---

## Part 1 — Get the dataset

We'll use the **PlantVillage** dataset on Kaggle (specifically the
"New Plant Diseases Dataset" by vipoooool), which already contains the
crops and diseases this project supports.

### 1a. Get a Kaggle API token (one-time setup)

1. Create a free account at kaggle.com if you don't have one.
2. Go to your account settings → **Create New API Token**. This downloads
   a file called `kaggle.json`.
3. Keep that file handy — you'll upload it in Colab in the next step.

### 1b. Download and reorganize the dataset (run this in Colab)

Open a new notebook at **colab.research.google.com**, then:

**Enable a GPU first:** `Runtime → Change runtime type → Hardware
accelerator → GPU → Save`.

Paste this into a cell and run it:

```python
# 1. Upload your kaggle.json when prompted
from google.colab import files
files.upload()  # select kaggle.json

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# 2. Download the dataset (~2GB, takes a few minutes)
!pip install -q kaggle
!kaggle datasets download -d vipoooool/new-plant-diseases-dataset
!unzip -q new-plant-diseases-dataset.zip -d plantvillage_raw
```

```python
# 3. Reorganize only the classes AgriDoctor AI uses, with the exact
#    folder names model.py expects, split into train/ and val/.
import os, shutil, random

SRC = "plantvillage_raw/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train"

# Maps PlantVillage's folder names -> this project's class names
CLASS_MAP = {
    "Tomato___Early_blight":                         "Tomato_Early_Blight",
    "Tomato___Late_blight":                          "Tomato_Late_Blight",
    "Tomato___Leaf_Mold":                             "Tomato_Leaf_Mold",
    "Tomato___healthy":                               "Tomato_Healthy",
    "Potato___Early_blight":                          "Potato_Early_Blight",
    "Potato___Late_blight":                           "Potato_Late_Blight",
    "Potato___healthy":                               "Potato_Healthy",
    "Corn_(maize)___Common_rust_":                    "Corn_Common_Rust",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Corn_Gray_Leaf_Spot",
    "Corn_(maize)___healthy":                         "Corn_Healthy",
}

VAL_SPLIT = 0.15
random.seed(42)

for src_name, dst_name in CLASS_MAP.items():
    src_dir = os.path.join(SRC, src_name)
    files_ = os.listdir(src_dir)
    random.shuffle(files_)
    n_val = int(len(files_) * VAL_SPLIT)
    val_files, train_files = files_[:n_val], files_[n_val:]

    for split, split_files in [("train", train_files), ("val", val_files)]:
        out_dir = f"data/{split}/{dst_name}"
        os.makedirs(out_dir, exist_ok=True)
        for f in split_files:
            shutil.copy(os.path.join(src_dir, f), os.path.join(out_dir, f))

    print(f"{dst_name}: {len(train_files)} train, {len(val_files)} val")
```

You should see 10 lines of output, one per class, each with a train/val
count. That confirms the folders are ready.

---

## Part 2 — Train the model

### Option A: Train in Colab (recommended)

```python
# Upload model.py and train_model.py from your project folder
from google.colab import files
files.upload()   # select model.py and train_model.py from AgriDoctor_AI_Prototype/
```

```python
!python train_model.py --data_dir data --epochs 15 --fine_tune_epochs 5
```

This uses the GPU automatically and should take well under an hour for
this dataset size (versus potentially many hours on a laptop CPU).

When it finishes, download the result:

```python
from google.colab import files
files.download("models/agridoctor_model.h5")
```

Save that downloaded file into your local project's `models/` folder,
replacing nothing else — `app.py` will detect it automatically next time
you run `streamlit run app.py`.

### Option B: Train locally instead

If you'd rather train on your own machine (slower, but no Colab needed):

1. Download the same dataset manually from Kaggle and unzip it.
2. Run the same reorganization Python snippet above locally (adjust `SRC`
   to wherever you unzipped it), so you end up with
   `AgriDoctor_AI_Prototype/data/train/<class>/...` and `data/val/<class>/...`.
3. From inside the project folder:
   ```
   python train_model.py --data_dir data --epochs 15 --fine_tune_epochs 5
   ```
4. Expect this to take a while on CPU — check Task Manager to confirm
   Python is actively using CPU (it's working, just slow), and consider
   starting with fewer epochs (`--epochs 5 --fine_tune_epochs 2`) first to
   confirm everything runs end-to-end before committing to a long run.

---

## After training

Once `models/agridoctor_model.h5` exists in your project folder:

1. Restart the app: `python -m streamlit run app.py`
2. The sidebar should now say **"Trained model loaded — running real
   predictions"** instead of the demo-mode warning.
3. Test with a few real leaf photos and compare results against demo mode's
   guesses — trained-mode results should be noticeably more consistent and
   accurate.

## If something goes wrong

- **"Could not find data/train"** — you're running `train_model.py` from
  the wrong folder, or the reorganization step didn't run. Check
  `ls data/train` shows 10 class folders.
- **Training seems stuck at "Epoch 1"** — normal on CPU; the first epoch is
  slowest. Give it a few minutes before assuming it's frozen.
- **Out of memory in Colab** — reduce `--batch_size` (e.g. `--batch_size 16`).
- **Class name mismatch warning when training starts** — double-check the
  folder names under `data/train/` exactly match the names in `CLASS_MAP`
  above (case-sensitive, matches `model.py`'s `CLASS_NAMES`).
