import json
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

from config import (
    CONFUSION_MATRIX_PATH,
    HISTORY_PATH,
    METRICS_PATH,
)


BASE_DIR = Path(__file__).resolve().parent.parent


st.set_page_config(
    page_title="Model Dashboard | EcoSort AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.html(
    """
    <style>

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at 8% 8%,
                rgba(53, 180, 91, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 92% 18%,
                rgba(53, 160, 83, 0.08),
                transparent 30%
            ),
            #06100a;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #09180e 0%,
                #06100a 100%
            );
        border-right: 1px solid rgba(100, 190, 120, 0.10);
    }

    .block-container {
        max-width: 1480px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 3.2rem;
        border-radius: 32px;
        background:
            linear-gradient(
                135deg,
                rgba(20, 70, 42, 0.98),
                rgba(6, 25, 15, 0.99)
            );
        border: 1px solid rgba(110, 205, 130, 0.22);
        box-shadow:
            0 25px 80px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.025);
        margin-bottom: 2rem;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        right: -100px;
        top: -130px;
        border-radius: 50%;
        background: rgba(101, 222, 126, 0.08);
    }

    .badge {
        display: inline-flex;
        padding: 0.45rem 0.85rem;
        border-radius: 999px;
        background: rgba(104, 218, 129, 0.10);
        border: 1px solid rgba(104, 218, 129, 0.22);
        color: #a4eab0;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        margin-bottom: 1rem;
    }

    .hero-title {
        color: #f0fff3;
        font-size: clamp(2.7rem, 5vw, 4.5rem);
        line-height: 0.98;
        font-weight: 900;
        letter-spacing: -0.06em;
        margin: 0;
        position: relative;
        z-index: 2;
    }

    .hero-title span {
        color: #76e090;
    }

    .hero-text {
        max-width: 850px;
        color: #a6c8b0;
        font-size: 1.04rem;
        line-height: 1.75;
        margin-top: 1.15rem;
        position: relative;
        z-index: 2;
    }

    .sidebar-brand {
        padding: 0.8rem 0 1.2rem;
        border-bottom: 1px solid rgba(100, 180, 120, 0.10);
        margin-bottom: 1.2rem;
    }

    .sidebar-title {
        color: #e9faed;
        font-size: 1.25rem;
        font-weight: 900;
    }

    .sidebar-subtitle {
        color: #779582;
        font-size: 0.75rem;
        margin-top: 0.25rem;
    }

    .status-card {
        padding: 0.9rem 1rem;
        border-radius: 15px;
        background: rgba(65, 181, 91, 0.08);
        border: 1px solid rgba(91, 198, 111, 0.15);
        color: #91d99d;
        font-size: 0.82rem;
        font-weight: 750;
    }

    .sidebar-section {
        color: #759381;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 800;
        margin-top: 1.4rem;
    }

    .sidebar-info {
        margin-top: 0.75rem;
        color: #b8d1be;
        line-height: 2;
        font-size: 0.82rem;
    }

    .section-title {
        color: #effbf2;
        font-size: 1.7rem;
        font-weight: 850;
        letter-spacing: -0.035em;
        margin-top: 2.7rem;
        margin-bottom: 0.8rem;
    }

    .section-subtitle {
        color: #819d89;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-top: -0.3rem;
        margin-bottom: 1.4rem;
    }

    .metric-wrapper {
        padding: 1.45rem;
        border-radius: 22px;
        background:
            linear-gradient(
                145deg,
                rgba(17, 45, 28, 0.97),
                rgba(8, 26, 16, 0.97)
            );
        border: 1px solid rgba(101, 174, 119, 0.16);
        min-height: 145px;
        box-sizing: border-box;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.12);
    }

    .metric-icon {
        font-size: 1.5rem;
    }

    .metric-label {
        color: #789883;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        font-weight: 850;
        margin-top: 0.45rem;
    }

    .metric-value {
        color: #eaf8ed;
        font-size: 2rem;
        font-weight: 900;
        margin-top: 0.25rem;
        letter-spacing: -0.045em;
    }

    .architecture-card {
        padding: 1.8rem;
        border-radius: 25px;
        background:
            linear-gradient(
                145deg,
                rgba(17, 45, 28, 0.97),
                rgba(8, 25, 16, 0.97)
            );
        border: 1px solid rgba(100, 163, 115, 0.16);
        min-height: 345px;
        box-sizing: border-box;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.12);
    }

    .architecture-icon {
        font-size: 2.1rem;
        margin-bottom: 0.8rem;
    }

    .architecture-title {
        color: #eaf8ed;
        font-size: 1.35rem;
        font-weight: 850;
        letter-spacing: -0.025em;
    }

    .architecture-text {
        color: #9eb9a6;
        line-height: 1.7;
        margin-top: 0.75rem;
    }

    .architecture-list {
        color: #b7cfbd;
        line-height: 1.95;
        margin-top: 1rem;
        padding-left: 1.15rem;
    }

    .training-card {
        padding: 1.4rem 1.5rem;
        border-radius: 22px;
        background:
            linear-gradient(
                145deg,
                rgba(17, 44, 27, 0.96),
                rgba(8, 25, 16, 0.96)
            );
        border: 1px solid rgba(100, 163, 115, 0.16);
        margin-bottom: 1.4rem;
    }

    .training-label {
        color: #789883;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 850;
    }

    .training-value {
        color: #72dc8b;
        font-size: 2.45rem;
        font-weight: 900;
        letter-spacing: -0.05em;
        margin-top: 0.2rem;
    }

    .training-description {
        color: #819d89;
        margin-top: 0.2rem;
        line-height: 1.5;
    }

    .chart-card {
        padding: 1rem;
        border-radius: 24px;
        background: rgba(10, 29, 19, 0.78);
        border: 1px solid rgba(100, 163, 115, 0.13);
        margin-bottom: 1.5rem;
    }

    .summary-card {
        padding: 1.45rem;
        border-radius: 22px;
        background:
            linear-gradient(
                145deg,
                rgba(15, 39, 24, 0.96),
                rgba(8, 25, 16, 0.96)
            );
        border: 1px solid rgba(98, 157, 110, 0.13);
        height: 100%;
        box-sizing: border-box;
    }

    .summary-icon {
        font-size: 1.5rem;
    }

    .summary-label {
        color: #789883;
        font-size: 0.73rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 850;
        margin-top: 0.5rem;
    }

    .summary-value {
        color: #eaf8ed;
        font-size: 1.8rem;
        font-weight: 900;
        margin-top: 0.25rem;
    }

    .summary-text {
        color: #819c88;
        font-size: 0.83rem;
        line-height: 1.6;
        margin-top: 0.35rem;
    }

    .evaluation-card {
        padding: 1.5rem;
        border-radius: 23px;
        background:
            linear-gradient(
                145deg,
                rgba(16, 42, 26, 0.95),
                rgba(8, 25, 16, 0.95)
            );
        border: 1px solid rgba(100, 163, 115, 0.14);
        height: 100%;
        box-sizing: border-box;
    }

    .evaluation-icon {
        font-size: 1.7rem;
    }

    .evaluation-title {
        color: #e7f5ea;
        font-size: 1.05rem;
        font-weight: 850;
        margin-top: 0.55rem;
    }

    .evaluation-text {
        color: #8fa996;
        line-height: 1.65;
        font-size: 0.84rem;
        margin-top: 0.45rem;
    }

    .notice {
        padding: 1.1rem 1.3rem;
        border-radius: 18px;
        background: rgba(23, 52, 32, 0.80);
        border: 1px solid rgba(104, 174, 119, 0.16);
        color: #9fbba7;
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }

    .footer-card {
        margin-top: 3.5rem;
        padding: 1.5rem;
        border-radius: 22px;
        background: rgba(15, 39, 24, 0.75);
        border: 1px solid rgba(96, 155, 108, 0.12);
        text-align: center;
        color: #789481;
        font-size: 0.82rem;
        line-height: 1.6;
    }

    </style>
    """
)


with st.sidebar:

    st.html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-title">
                ♻️ EcoSort AI
            </div>
            <div class="sidebar-subtitle">
                Model Intelligence Dashboard
            </div>
        </div>
        """
    )

    st.html(
        """
        <div class="status-card">
            ● Trained model loaded
        </div>
        """
    )

    st.html(
        """
        <div class="sidebar-section">
            Architecture
        </div>

        <div class="sidebar-info">
            <b>EfficientNetB0</b><br>
            ImageNet Transfer Learning<br>
            224 × 224 Input<br>
            9-Class Softmax
        </div>
        """
    )

    st.html(
        """
        <div class="sidebar-section">
            Training
        </div>

        <div class="sidebar-info">
            8,235 Images<br>
            80 / 20 Stratified Split<br>
            8 + 12 Epochs<br>
            NVIDIA Tesla T4
        </div>
        """
    )

    st.html(
        """
        <div class="sidebar-section">
            Optimization
        </div>

        <div class="sidebar-info">
            Adam Optimizer<br>
            Initial LR: 0.001<br>
            Fine-Tune LR: 1e-5<br>
            Dropout: 0.3
        </div>
        """
    )


st.html(
    """
    <div class="hero">

        <div class="badge">
            📊 ECO SORT AI · MODEL INTELLIGENCE
        </div>

        <h1 class="hero-title">
            Measure the <span>model.</span>
        </h1>

        <div class="hero-text">
            Explore EcoSort AI's classification performance, training
            behaviour, transfer-learning strategy, validation results,
            confusion matrix, and evaluation metrics.
        </div>

    </div>
    """
)


if not METRICS_PATH.exists():

    st.html(
        """
        <div class="notice">
            ⚠️ Model metrics are not available.
            Make sure the trained model output files are present
            inside the <strong>model</strong> directory.
        </div>
        """
    )

    st.stop()


try:

    with open(
        METRICS_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        metrics = json.load(file)

except (
    OSError,
    json.JSONDecodeError,
):

    st.error(
        "The model metrics file could not be read."
    )

    st.stop()


accuracy = float(
    metrics.get(
        "accuracy",
        0,
    )
)

precision = float(
    metrics.get(
        "precision",
        0,
    )
)

recall = float(
    metrics.get(
        "recall",
        0,
    )
)

f1_score_value = float(
    metrics.get(
        "f1_score",
        0,
    )
)


st.html(
    '<div class="section-title">🎯 Validation Performance</div>'
)

st.html(
    """
    <div class="section-subtitle">
        Final weighted validation metrics from the nine-class waste classification task.
    </div>
    """
)


c1, c2, c3, c4 = st.columns(
    4,
    gap="medium",
)


metric_data = [
    (
        c1,
        "🎯",
        "Accuracy",
        accuracy,
    ),
    (
        c2,
        "🔎",
        "Precision",
        precision,
    ),
    (
        c3,
        "📌",
        "Recall",
        recall,
    ),
    (
        c4,
        "⚖️",
        "F1 Score",
        f1_score_value,
    ),
]


for column, icon, label, value in metric_data:

    with column:

        st.html(
            f"""
            <div class="metric-wrapper">

                <div class="metric-icon">
                    {icon}
                </div>

                <div class="metric-label">
                    {label}
                </div>

                <div class="metric-value">
                    {value * 100:.2f}%
                </div>

            </div>
            """
        )


st.html(
    '<div class="section-title">🧠 Model Architecture</div>'
)

st.html(
    """
    <div class="section-subtitle">
        Technical configuration used to develop the final EcoSort AI classifier.
    </div>
    """
)


c1, c2 = st.columns(
    2,
    gap="large",
)


with c1:

    st.html(
        """
        <div class="architecture-card">

            <div class="architecture-icon">
                🧠
            </div>

            <div class="architecture-title">
                EfficientNetB0
            </div>

            <div class="architecture-text">
                EcoSort AI uses an ImageNet-pretrained EfficientNetB0
                convolutional backbone for nine-class waste image
                classification.
            </div>

            <ul class="architecture-list">
                <li>ImageNet pretrained weights</li>
                <li>224 × 224 × 3 input</li>
                <li>Global Average Pooling</li>
                <li>Batch Normalization</li>
                <li>Dropout = 0.3</li>
                <li>9-unit Dense Softmax output</li>
                <li>Transfer learning approach</li>
            </ul>

        </div>
        """
    )


with c2:

    st.html(
        """
        <div class="architecture-card">

            <div class="architecture-icon">
                🚀
            </div>

            <div class="architecture-title">
                Two-Phase Transfer Learning
            </div>

            <div class="architecture-text">
                Training was performed in two phases, beginning with
                classification-head training followed by fine-tuning
                of the EfficientNetB0 backbone.
            </div>

            <ul class="architecture-list">
                <li>Phase 1: 8 epochs</li>
                <li>Phase 2: 12 epochs</li>
                <li>Initial LR: 0.001</li>
                <li>Fine-tuning LR: 1e-5</li>
                <li>First 70% of backbone frozen</li>
                <li>Remaining 30% fine-tuned</li>
                <li>Adam optimizer</li>
            </ul>

        </div>
        """
    )


if HISTORY_PATH.exists():

    try:

        with open(
            HISTORY_PATH,
            "r",
            encoding="utf-8",
        ) as file:

            history = json.load(file)

    except (
        OSError,
        json.JSONDecodeError,
    ):

        history = {}

else:

    history = {}


accuracy_history = history.get(
    "accuracy",
    [],
)

validation_accuracy = history.get(
    "val_accuracy",
    [],
)

loss_history = history.get(
    "loss",
    [],
)

validation_loss = history.get(
    "val_loss",
    [],
)


epochs = len(
    accuracy_history
)


st.html(
    '<div class="section-title">📈 Training Behaviour</div>'
)

st.html(
    """
    <div class="section-subtitle">
        Accuracy and loss recorded throughout the two-phase training process.
    </div>
    """
)


if epochs:

    st.html(
        f"""
        <div class="training-card">

            <div class="training-label">
                Training History
            </div>

            <div class="training-value">
                {epochs}
            </div>

            <div class="training-description">
                Recorded epochs across initial training and fine-tuning.
            </div>

        </div>
        """
    )


if accuracy_history:

    figure, axis = plt.subplots(
        figsize=(10, 5)
    )

    epoch_numbers = range(
        1,
        len(accuracy_history) + 1,
    )

    axis.plot(
        epoch_numbers,
        accuracy_history,
        label="Training Accuracy",
        linewidth=2.5,
    )

    if validation_accuracy:

        axis.plot(
            range(
                1,
                len(validation_accuracy) + 1,
            ),
            validation_accuracy,
            label="Validation Accuracy",
            linewidth=2.5,
        )

    axis.set_xlabel(
        "Epoch"
    )

    axis.set_ylabel(
        "Accuracy"
    )

    axis.set_title(
        "Training vs Validation Accuracy"
    )

    axis.set_ylim(
        0,
        1,
    )

    axis.grid(
        alpha=0.2
    )

    axis.legend()

    figure.tight_layout()

    st.pyplot(
        figure,
        width="stretch",
    )

    plt.close(
        figure
    )


if loss_history:

    figure, axis = plt.subplots(
        figsize=(10, 5)
    )

    epoch_numbers = range(
        1,
        len(loss_history) + 1,
    )

    axis.plot(
        epoch_numbers,
        loss_history,
        label="Training Loss",
        linewidth=2.5,
    )

    if validation_loss:

        axis.plot(
            range(
                1,
                len(validation_loss) + 1,
            ),
            validation_loss,
            label="Validation Loss",
            linewidth=2.5,
        )

    axis.set_xlabel(
        "Epoch"
    )

    axis.set_ylabel(
        "Loss"
    )

    axis.set_title(
        "Training vs Validation Loss"
    )

    axis.grid(
        alpha=0.2
    )

    axis.legend()

    figure.tight_layout()

    st.pyplot(
        figure,
        width="stretch",
    )

    plt.close(
        figure
    )


if not accuracy_history and not loss_history:

    st.html(
        """
        <div class="notice">
            ℹ️ Training history is not available.
            The model metrics are available, but training curves
            cannot be displayed.
        </div>
        """
    )


st.html(
    '<div class="section-title">🔢 Confusion Matrix</div>'
)

st.html(
    """
    <div class="section-subtitle">
        Validation-set prediction behaviour across all nine waste categories.
    </div>
    """
)


if CONFUSION_MATRIX_PATH.exists():

    st.image(
        CONFUSION_MATRIX_PATH,
        caption="EcoSort AI Validation Set Confusion Matrix",
        width="stretch",
    )

else:

    st.html(
        """
        <div class="notice">
            ℹ️ Confusion matrix image is not available.
        </div>
        """
    )


st.html(
    '<div class="section-title">🧪 Evaluation Methodology</div>'
)

st.html(
    """
    <div class="section-subtitle">
        Key methodological details behind the reported validation results.
    </div>
    """
)


c1, c2, c3 = st.columns(
    3,
    gap="medium",
)


with c1:

    st.html(
        """
        <div class="evaluation-card">

            <div class="evaluation-icon">
                🗂️
            </div>

            <div class="evaluation-title">
                Stratified Validation
            </div>

            <div class="evaluation-text">
                The dataset was divided into 80% training and 20%
                validation using stratified sampling to preserve
                class proportions.
            </div>

        </div>
        """
    )


with c2:

    st.html(
        """
        <div class="evaluation-card">

            <div class="evaluation-icon">
                🎯
            </div>

            <div class="evaluation-title">
                Nine-Class Classification
            </div>

            <div class="evaluation-text">
                The model performs single-stage multiclass classification
                using nine Softmax output classes.
            </div>

        </div>
        """
    )


with c3:

    st.html(
        """
        <div class="evaluation-card">

            <div class="evaluation-icon">
                📊
            </div>

            <div class="evaluation-title">
                Validation Metrics
            </div>

            <div class="evaluation-text">
                Accuracy, weighted precision, weighted recall,
                weighted F1-score, and confusion matrix are used
                to evaluate model performance.
            </div>

        </div>
        """
    )


st.html(
    '<div class="section-title">📋 Model Summary</div>'
)


c1, c2, c3, c4 = st.columns(
    4,
    gap="medium",
)


with c1:

    st.html(
        """
        <div class="summary-card">

            <div class="summary-icon">
                🗂️
            </div>

            <div class="summary-label">
                Classes
            </div>

            <div class="summary-value">
                9
            </div>

            <div class="summary-text">
                Waste categories classified by EcoSort AI.
            </div>

        </div>
        """
    )


with c2:

    st.html(
        """
        <div class="summary-card">

            <div class="summary-icon">
                🖼️
            </div>

            <div class="summary-label">
                Images Used
            </div>

            <div class="summary-value">
                8,235
            </div>

            <div class="summary-text">
                Images used for model development.
            </div>

        </div>
        """
    )


with c3:

    st.html(
        """
        <div class="summary-card">

            <div class="summary-icon">
                📐
            </div>

            <div class="summary-label">
                Input
            </div>

            <div class="summary-value">
                224²
            </div>

            <div class="summary-text">
                Image resolution used by EfficientNetB0.
            </div>

        </div>
        """
    )


with c4:

    st.html(
        """
        <div class="summary-card">

            <div class="summary-icon">
                💻
            </div>

            <div class="summary-label">
                Hardware
            </div>

            <div class="summary-value">
                T4 GPU
            </div>

            <div class="summary-text">
                NVIDIA Tesla T4 used for model training.
            </div>

        </div>
        """
    )


st.html(
    """
    <div class="footer-card">

        <strong style="color:#a8c7af;">
            EcoSort AI
        </strong>

        <br>

        Intelligent Waste Classification · Model Evaluation ·
        Sustainable Technology

    </div>
    """
)