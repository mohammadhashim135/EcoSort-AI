# ♻️ EcoSort AI

An AI-powered waste classification and sustainability intelligence system built with **TensorFlow, EfficientNetB0, and Streamlit**.

EcoSort AI classifies waste images into **nine categories** and provides sustainability information, recommended recovery actions, environmental impact indicators, and relevant SDG connections.

---

## 🚀 Features

* 🤖 AI-powered waste image classification
* ♻️ Nine-class waste classification
* 🧠 EfficientNetB0 transfer learning
* 🎯 92.96% validation accuracy
* 📊 Precision, recall, F1-score, and confusion matrix
* 📈 Training and validation curves
* 🌱 Sustainability information for each category
* 🌍 Environmental impact indicators
* ♻️ Recommended recovery actions
* 🌐 SDG-related information
* 🖼️ Image upload and real-time classification
* 📋 Top-3 prediction probabilities
* 🎨 Dark-green Streamlit interface
* 📱 Multi-page dashboard

---

## 🧠 Model

EcoSort AI uses **EfficientNetB0** with ImageNet pretrained weights as the backbone.

The model performs multiclass classification across nine waste categories:

1. Aluminium
2. Carton
3. E-waste
4. Glass
5. Organic Waste
6. Paper & Cardboard
7. Plastics
8. Textiles
9. Wood

The final classification layer contains **9 Softmax outputs**.

---

## 📊 Model Performance

| Metric    |      Score |
| --------- | ---------: |
| Accuracy  | **92.96%** |
| Precision | **93.00%** |
| Recall    | **92.96%** |
| F1 Score  | **92.97%** |

### Class-wise Performance

| Waste Category    | Precision | Recall | F1 Score |
| ----------------- | --------: | -----: | -------: |
| Aluminium         |       94% |    93% |      94% |
| Carton            |       94% |    93% |      94% |
| E-waste           |       91% |    93% |      92% |
| Glass             |       92% |    92% |      92% |
| Organic Waste     |       99% |    96% |      97% |
| Paper & Cardboard |       91% |    93% |      92% |
| Plastics          |       89% |    89% |      89% |
| Textiles          |       96% |    96% |      96% |
| Wood              |       92% |    94% |      93% |

---

## 🧪 Training Configuration

| Configuration             | Value               |
| ------------------------- | ------------------- |
| Architecture              | EfficientNetB0      |
| Pretrained Weights        | ImageNet            |
| Input Size                | 224 × 224 × 3       |
| Classes                   | 9                   |
| Dataset Images Used       | 8,235               |
| Training Images           | 6,588               |
| Validation Images         | 1,647               |
| Split                     | 80% / 20%           |
| Split Method              | Stratified          |
| Initial Training          | 8 epochs            |
| Fine-Tuning               | 12 epochs           |
| Maximum Epochs            | 20                  |
| Optimizer                 | Adam                |
| Initial Learning Rate     | 0.001               |
| Fine-Tuning Learning Rate | 1e-5                |
| Dropout                   | 0.3                 |
| Fine-Tuning               | Top 30% of backbone |
| Training Hardware         | NVIDIA Tesla T4     |

---

## 🖼️ Preprocessing & Augmentation

Images are resized to **224 × 224 pixels**.

Training augmentation includes:

* Random horizontal flipping
* Random rotation
* Random zoom
* Random contrast adjustment

The validation dataset is not augmented.

The dataset uses an **80/20 stratified split** to preserve class distribution.

---

## 🗂️ Dataset

The dataset was obtained from **Kaggle**.

The original dataset contained:

- 8,346 images
- 9 waste categories

After data preparation and cleaning, **8,235 images** were used for model development.

The dataset is not included in this repository because of its size.

### Dataset Link

[Kaggle Dataset](https://www.kaggle.com/datasets/angelikasita/waste-images)

Expected folder structure:

```bash
data/
├── Aluminium/
├── Carton/
├── E-waste/
├── Glass/
├── Organic_Waste/
├── Paper_and_Cardboard/
├── Plastics/
├── Textiles/
└── Wood/
```

---

## 📂 Project Structure

```bash
EcoSort-AI/
│
├── data/
│   └── Dataset not included in repository
│
├── model/
│   ├── ecosort.keras
│   ├── class_names.json
│   ├── history.json
│   ├── metrics.json
│   └── confusion_matrix.png
│
├── pages/
│   ├── 1_Classify_Waste.py
│   ├── 2_Sustainability.py
│   └── 3_Model_Dashboard.py
│
├── assets/
│   ├── 3.png
│   ├── 6.jpg
│   ├── 7.png
│   ├── 12.png
│   ├── 13.png
│   ├── 14.png
│   └── 15.png
│
├── app.py
├── train.py
├── config.py
├── sustainability.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| Python         | Core programming language       |
| TensorFlow     | Deep learning framework         |
| Keras          | Model development and inference |
| EfficientNetB0 | Image classification            |
| Streamlit      | Web application and dashboard   |
| NumPy          | Numerical computing             |
| Pandas         | Data processing                 |
| Scikit-learn   | Model evaluation                |
| Matplotlib     | Visualization                   |
| Pillow         | Image processing                |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mohammadhashim135/EcoSort-AI.git
cd EcoSort-AI
```

### 2. Create a Virtual Environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📱 Application Pages

### 🏠 Home

Provides an overview of:

* Project introduction
* Model performance
* Dataset statistics
* Model configuration
* Sustainability focus
* Supported waste categories
* SDG connections

### 🤖 Waste Classification

Users can upload an image of waste and receive:

* Predicted waste category
* Prediction confidence
* Top-3 predictions
* Sustainability information
* Environmental impact indicator
* Recommended recovery action
* Waste-management guidance
* Related SDGs

Supported image formats:

```bash
JPG
JPEG
PNG
WEBP
```

### 🌱 Sustainability

Provides category-specific information including:

* Environmental impact level
* Impact score
* Recyclability
* Material profile
* Recommended recovery action
* Practical guidance
* Related SDGs

The environmental impact score is a **category-level sustainability indicator**, not a direct measurement of carbon emissions.

### 📊 Model Dashboard

Provides technical information about the trained model, including:

* Validation accuracy
* Precision, recall, and F1 score
* Model architecture
* Training configuration
* Accuracy curves
* Loss curves
* Confusion matrix
* Evaluation methodology
* Model summary

---

## 🔬 Transfer Learning Strategy

EcoSort AI uses a two-phase transfer learning approach.

### Phase 1 — Initial Training

The ImageNet-pretrained EfficientNetB0 backbone is frozen while the classification layers are trained.

```bash
Epochs: 8
Learning Rate: 0.001
Optimizer: Adam
```

### Phase 2 — Fine-Tuning

The upper portion of the EfficientNetB0 backbone is unfrozen and fine-tuned using a lower learning rate.

```bash
Epochs: 12
Learning Rate: 1e-5
Optimizer: Adam
```

This allows the model to adapt pretrained visual features to waste classification while reducing the risk of damaging useful pretrained representations.

---

## 📊 Evaluation

The model was evaluated using the validation portion of the dataset.

Evaluation includes:

* Accuracy
* Weighted precision
* Weighted recall
* Weighted F1 score
* Class-wise precision, recall, and F1
* Confusion matrix
* Training and validation accuracy
* Training and validation loss

The reported results are based on the validation set. **No independent external test dataset was used for final evaluation.**

---

## ♻️ Sustainability Intelligence

EcoSort AI connects waste classification with sustainability guidance.

The system provides recovery information for:

* Aluminium
* Carton
* E-waste
* Glass
* Organic Waste
* Paper & Cardboard
* Plastics
* Textiles
* Wood

Recommended recovery pathways may include:

* Recycling
* Reuse
* Donation
* Composting
* Specialized e-waste collection
* Material recovery

Actual disposal and recycling options depend on local waste-management infrastructure and regulations.

---

## 🌍 Sustainable Development Goals

EcoSort AI provides contextual connections to selected **United Nations Sustainable Development Goals (SDGs)**:

* **SDG 3** — Good Health and Well-being
* **SDG 6** — Clean Water and Sanitation
* **SDG 7** — Affordable and Clean Energy
* **SDG 12** — Responsible Consumption and Production
* **SDG 13** — Climate Action
* **SDG 14** — Life Below Water
* **SDG 15** — Life on Land

These are **contextual sustainability mappings**, not calculated SDG performance metrics.

---

## 📈 Model Artifacts

The trained model and evaluation files are stored in the `model/` directory.

```bash
model/
├── ecosort.keras
├── class_names.json
├── history.json
├── metrics.json
└── confusion_matrix.png
```

| File                   | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `ecosort.keras`        | Trained EfficientNetB0-based classification model |
| `class_names.json`     | Nine class labels                                 |
| `history.json`         | Training and validation history                   |
| `metrics.json`         | Final validation metrics                          |
| `confusion_matrix.png` | Validation confusion matrix                       |

---

## 🏋️ Retraining the Model

The training script is included for reproducibility.

First, download the dataset from the Kaggle link and place it inside the `data/` directory.

Then run:

```bash
python3 train.py
```

The trained model and evaluation artifacts will be generated in the project directories.

---
## **Contributing** 🤝
Contributions are welcome! If you’d like to improve feel free to fork the repo and submit a pull request.

### **Steps to Contribute:**

### **1. Fork the repository**

### **2. Create a new branch:**

```bash
git checkout -b feature-branch
```

### **3. Make your changes and commit:**

```bash
git commit -m "Added new feature"
```
### **4. Push to the branch:**

```bash
git push origin feature-branch
```
### **5. Open a Pull Request**
---
## **License** 📜
This project is licensed under the MIT License.

💡 Developed with ❤️ by [Mohammad Hashim](https://github.com/mohammadhashim135/EcoSort-AI.git)
