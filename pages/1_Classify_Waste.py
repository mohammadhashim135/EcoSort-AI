import base64
import html
import json
from pathlib import Path

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

from config import (
    CLASS_NAMES_PATH,
    IMAGE_SIZE,
    MODEL_PATH,
)

from sustainability import get_sustainability_data


st.set_page_config(
    page_title="Classify Waste | EcoSort AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)


BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"


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

    .block-container {
        max-width: 1480px;
        padding-top: 2rem;
        padding-bottom: 4rem;
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

    [data-testid="stSidebar"] * {
        color: #c8dfce;
    }

    .page-header {
        position: relative;
        overflow: hidden;
        padding: 3rem 3.2rem;
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

    .page-header::after {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        right: -90px;
        top: -110px;
        border-radius: 50%;
        background: rgba(101, 222, 126, 0.08);
        filter: blur(4px);
    }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
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

    .page-title {
        font-size: clamp(2.8rem, 5vw, 4.5rem);
        line-height: 0.98;
        font-weight: 900;
        letter-spacing: -0.06em;
        color: #f0fff3;
        margin: 0;
        position: relative;
        z-index: 2;
    }

    .page-title span {
        color: #76e090;
    }

    .page-subtitle {
        max-width: 820px;
        color: #a6c8b0;
        font-size: 1.04rem;
        line-height: 1.75;
        margin-top: 1.1rem;
        position: relative;
        z-index: 2;
    }

    .upload-card {
        padding: 1.7rem 1.9rem;
        border-radius: 25px;
        background:
            linear-gradient(
                145deg,
                rgba(17, 45, 28, 0.96),
                rgba(7, 24, 15, 0.97)
            );
        border: 1px solid rgba(100, 175, 116, 0.17);
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.16);
        margin-bottom: 1rem;
    }

    .upload-title {
        color: #effbf1;
        font-size: 1.3rem;
        font-weight: 850;
    }

    .upload-text {
        color: #89a994;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-top: 0.35rem;
    }

    [data-testid="stFileUploader"] {
        border-radius: 22px;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: rgba(11, 30, 18, 0.80);
        border: 1px dashed rgba(103, 190, 123, 0.25);
        border-radius: 22px;
        padding: 1rem;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: rgba(115, 220, 137, 0.48);
        background: rgba(15, 39, 23, 0.90);
    }

    .section-title {
        color: #effbf2;
        font-size: 1.65rem;
        font-weight: 850;
        letter-spacing: -0.035em;
        margin-top: 2.5rem;
        margin-bottom: 0.8rem;
    }

    .section-subtitle {
        color: #829f8b;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-top: -0.35rem;
        margin-bottom: 1.25rem;
    }

    .image-card {
        padding: 0.7rem;
        border-radius: 25px;
        background:
            linear-gradient(
                145deg,
                rgba(14, 37, 22, 0.98),
                rgba(7, 21, 13, 0.98)
            );
        border: 1px solid rgba(100, 166, 116, 0.17);
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.18);
    }

    .image-info {
        margin-top: 0.8rem;
        padding: 0.9rem 1rem;
        border-radius: 16px;
        background: rgba(12, 32, 19, 0.88);
        border: 1px solid rgba(95, 154, 107, 0.12);
        color: #89a592;
        font-size: 0.78rem;
    }

    .result-card {
        padding: 2rem;
        border-radius: 27px;
        background:
            linear-gradient(
                145deg,
                rgba(20, 66, 40, 0.98),
                rgba(7, 27, 16, 0.99)
            );
        border: 1px solid rgba(105, 205, 128, 0.25);
        box-shadow:
            0 25px 65px rgba(0, 0, 0, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.025);
    }

    .result-label {
        color: #8db398;
        font-size: 0.73rem;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        font-weight: 850;
    }

    .result-name {
        color: #f2fff4;
        font-size: clamp(2.2rem, 4vw, 3rem);
        line-height: 1.05;
        font-weight: 900;
        letter-spacing: -0.05em;
        margin-top: 0.55rem;
    }

    .confidence-wrap {
        margin-top: 1.3rem;
    }

    .confidence-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.45rem;
    }

    .confidence-label {
        color: #87a990;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .confidence-number {
        color: #76e091;
        font-size: 1.5rem;
        font-weight: 900;
    }

    .confidence-track {
        height: 9px;
        width: 100%;
        border-radius: 99px;
        background: rgba(255, 255, 255, 0.07);
        overflow: hidden;
    }

    .confidence-fill {
        height: 100%;
        border-radius: 99px;
        background: linear-gradient(
            90deg,
            #4cbf6b,
            #7ae394
        );
    }

    .action-box {
        margin-top: 1.5rem;
        padding: 1.05rem 1.15rem;
        border-radius: 17px;
        background: rgba(102, 205, 125, 0.08);
        border: 1px solid rgba(102, 205, 125, 0.17);
    }

    .action-label {
        color: #82aa8e;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        font-weight: 850;
    }

    .action-value {
        color: #e2f8e7;
        font-size: 1rem;
        font-weight: 800;
        margin-top: 0.3rem;
        line-height: 1.5;
    }

    .metric-card {
        padding: 1.35rem;
        border-radius: 21px;
        background:
            linear-gradient(
                145deg,
                rgba(17, 44, 27, 0.96),
                rgba(8, 26, 16, 0.96)
            );
        border: 1px solid rgba(100, 166, 115, 0.15);
        text-align: center;
        height: 100%;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.10);
    }

    .metric-icon {
        font-size: 1.55rem;
    }

    .metric-title {
        color: #82a38b;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        font-weight: 850;
        margin-top: 0.45rem;
    }

    .metric-value {
        color: #ecfaef;
        font-size: 1.2rem;
        font-weight: 850;
        margin-top: 0.35rem;
    }

    .prediction-card {
        padding: 1.05rem 1.2rem;
        border-radius: 18px;
        background: rgba(12, 32, 20, 0.92);
        border: 1px solid rgba(95, 151, 108, 0.13);
        margin-bottom: 0.45rem;
    }

    .prediction-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
    }

    .prediction-name {
        color: #e6f4e9;
        font-weight: 800;
    }

    .prediction-score {
        color: #79dc90;
        font-weight: 850;
    }

    .profile-card {
        padding: 1.45rem;
        border-radius: 21px;
        background:
            linear-gradient(
                145deg,
                rgba(17, 44, 28, 0.96),
                rgba(9, 26, 17, 0.96)
            );
        border: 1px solid rgba(101, 160, 114, 0.15);
        height: 100%;
    }

    .profile-label {
        color: #789983;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        font-weight: 850;
    }

    .profile-value {
        color: #eaf8ed;
        font-size: 1.1rem;
        font-weight: 850;
        margin-top: 0.45rem;
        line-height: 1.45;
    }

    .description-card {
        padding: 1.4rem 1.5rem;
        border-radius: 20px;
        background: rgba(16, 39, 25, 0.86);
        border: 1px solid rgba(100, 160, 113, 0.14);
        color: #a8c2ae;
        line-height: 1.75;
    }

    .carbon-card {
        padding: 1.5rem;
        border-radius: 22px;
        background:
            linear-gradient(
                135deg,
                rgba(24, 65, 39, 0.58),
                rgba(10, 30, 18, 0.92)
            );
        border: 1px solid rgba(103, 190, 122, 0.18);
    }

    .carbon-title {
        color: #dff5e4;
        font-weight: 850;
        font-size: 1.08rem;
    }

    .carbon-text {
        color: #9ab6a2;
        line-height: 1.7;
        margin-top: 0.6rem;
    }

    .tip-card {
        padding: 0.95rem 1.1rem;
        border-radius: 16px;
        background: rgba(13, 34, 21, 0.90);
        border: 1px solid rgba(98, 157, 110, 0.12);
        color: #b4cdbb;
        margin-bottom: 0.65rem;
        line-height: 1.55;
    }

    .sdg-card {
        padding: 1rem;
        border-radius: 20px;
        background:
            linear-gradient(
                145deg,
                rgba(12, 36, 23, 0.97),
                rgba(7, 25, 16, 0.97)
            );
        border: 1px solid rgba(100, 160, 113, 0.14);
        text-align: center;
        min-height: 225px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.14);
    }

    .sdg-image {
        width: 125px;
        height: 125px;
        object-fit: contain;
        border-radius: 14px;
        display: block;
        margin: 0 auto;
    }

    .sdg-name {
        color: #dceee0;
        font-weight: 850;
        margin-top: 0.65rem;
    }

    .sdg-description {
        color: #789683;
        font-size: 0.76rem;
        margin-top: 0.2rem;
        line-height: 1.45;
    }

    .empty-state {
        padding: 4.5rem 2rem;
        border-radius: 28px;
        background:
            linear-gradient(
                145deg,
                rgba(16, 42, 26, 0.94),
                rgba(8, 25, 16, 0.97)
            );
        border: 1px solid rgba(100, 164, 115, 0.16);
        text-align: center;
        margin-top: 1rem;
    }

    .empty-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    .empty-title {
        color: #edf9f0;
        font-size: 1.6rem;
        font-weight: 850;
    }

    .empty-text {
        color: #819d89;
        max-width: 600px;
        margin: 0.65rem auto 0;
        line-height: 1.7;
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

    .footer-card {
        margin-top: 3.5rem;
        padding: 1.4rem;
        border-radius: 21px;
        background: rgba(15, 39, 24, 0.76);
        border: 1px solid rgba(96, 155, 108, 0.12);
        text-align: center;
        color: #789481;
        font-size: 0.8rem;
        line-height: 1.6;
    }

    </style>
    """
)


@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)


@st.cache_data
def load_classes():
    with open(
        CLASS_NAMES_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


if not MODEL_PATH.exists():
    st.error(
        "Model not found. Make sure model/ecosort.keras exists."
    )
    st.stop()


if not CLASS_NAMES_PATH.exists():
    st.error(
        "Class names file not found. Make sure model/class_names.json exists."
    )
    st.stop()


try:
    model = load_model()
    class_names = load_classes()
except Exception as error:
    st.error(
        f"Unable to load the EcoSort AI model: {error}"
    )
    st.stop()


if len(class_names) != model.output_shape[-1]:
    st.error(
        "The number of class names does not match the model output."
    )
    st.stop()


with st.sidebar:
    st.html(
        """
        <div style="
            padding:0.8rem 0 1.2rem;
            border-bottom:1px solid rgba(100,180,120,0.10);
            margin-bottom:1.2rem;
        ">
            <div style="
                color:#e9faed;
                font-size:1.25rem;
                font-weight:900;
            ">
                ♻️ EcoSort AI
            </div>

            <div style="
                color:#779582;
                font-size:0.75rem;
                margin-top:0.25rem;
            ">
                Intelligent Waste Classification
            </div>
        </div>
        """
    )

    st.html(
        """
        <div class="status-card">
            ● AI model ready
        </div>
        """
    )

    st.html(
        """
        <div style="
            margin-top:1.4rem;
            color:#759381;
            font-size:0.7rem;
            text-transform:uppercase;
            letter-spacing:0.1em;
            font-weight:800;
        ">
            Model information
        </div>

        <div style="
            margin-top:0.8rem;
            color:#c5ddcb;
            line-height:2;
            font-size:0.82rem;
        ">
            <b>Architecture:</b> EfficientNetB0<br>
            <b>Input:</b> 224 × 224<br>
            <b>Classes:</b> 9<br>
            <b>Output:</b> Softmax
        </div>
        """
    )


st.html(
    """
    <div class="page-header">

        <div class="badge">
            ♻️ ECO SORT AI · COMPUTER VISION
        </div>

        <h1 class="page-title">
            Classify <span>Waste.</span>
        </h1>

        <div class="page-subtitle">
            Upload a photo of a waste item and let EcoSort AI
            identify its material, estimate prediction confidence,
            and transform the result into a practical sustainability action.
        </div>

    </div>
    """
)


st.html(
    """
    <div class="upload-card">

        <div class="upload-title">
            📷 Upload your waste image
        </div>

        <div class="upload-text">
            Use a clear, well-lit image where the waste item is
            visible. Supported formats: JPG, JPEG, PNG and WEBP.
        </div>

    </div>
    """
)


uploaded_file = st.file_uploader(
    "Choose an image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
    ],
    label_visibility="collapsed",
)


if uploaded_file is None:
    st.html(
        """
        <div class="empty-state">

            <div class="empty-icon">
                📸
            </div>

            <div class="empty-title">
                Ready to analyse your waste
            </div>

            <div class="empty-text">
                Upload an image to receive an AI classification,
                confidence score, top predictions, sustainability
                information, disposal guidance and related SDGs.
            </div>

        </div>
        """
    )

    st.stop()


try:
    image = Image.open(uploaded_file).convert("RGB")
except Exception:
    st.error(
        "The uploaded file could not be read as an image."
    )
    st.stop()


left, right = st.columns(
    [1.05, 0.95],
    gap="large",
)


with left:
    st.html(
        """
        <div class="section-title">
            Uploaded image
        </div>
        """
    )

    image_data = base64.b64encode(
        uploaded_file.getvalue()
    ).decode("utf-8")

    st.html(
        f"""
        <div class="image-card">

            <img
                src="data:image/{uploaded_file.type.split('/')[-1]};base64,{image_data}"
                style="
                    width:100%;
                    max-height:620px;
                    object-fit:contain;
                    display:block;
                    border-radius:18px;
                    background:#08140c;
                "
                alt="Uploaded waste image"
            >

        </div>
        """
    )

    st.html(
        f"""
        <div class="image-info">
            📄 <b>File:</b> {html.escape(uploaded_file.name)}
            &nbsp; · &nbsp;
            📐 <b>Size:</b> {image.width} × {image.height}px
            &nbsp; · &nbsp;
            💾 <b>Format:</b> {html.escape(uploaded_file.type)}
        </div>
        """
    )


with right:
    st.html(
        """
        <div class="section-title">
            AI analysis
        </div>
        """
    )

    resized_image = image.resize(
        IMAGE_SIZE
    )

    image_array = np.asarray(
        resized_image,
        dtype=np.float32,
    )

    image_array = np.expand_dims(
        image_array,
        axis=0,
    )

    with st.spinner(
        "Analysing image..."
    ):
        predictions = model.predict(
            image_array,
            verbose=0,
        )[0]

    predictions = np.asarray(
        predictions,
        dtype=np.float32,
    )

    top_indices = np.argsort(
        predictions
    )[::-1]

    predicted_index = int(
        top_indices[0]
    )

    predicted_class = class_names[
        predicted_index
    ]

    confidence = float(
        predictions[predicted_index]
    )

    sustainability = get_sustainability_data(
        predicted_class
    )

    display_name = sustainability.get(
        "display_name",
        predicted_class.replace("_", " "),
    )

    icon = sustainability.get(
        "icon",
        "♻️",
    )

    action = sustainability.get(
        "action",
        "Follow local disposal guidance.",
    )

    safe_display_name = html.escape(
        str(display_name)
    )

    safe_action = html.escape(
        str(action)
    )

    confidence_percent = confidence * 100

    st.html(
        f"""
        <div class="result-card">

            <div class="result-label">
                Detected waste type
            </div>

            <div class="result-name">
                {html.escape(str(icon))} {safe_display_name}
            </div>

            <div class="confidence-wrap">

                <div class="confidence-row">

                    <div class="confidence-label">
                        AI prediction confidence
                    </div>

                    <div class="confidence-number">
                        {confidence_percent:.2f}%
                    </div>

                </div>

                <div class="confidence-track">
                    <div
                        class="confidence-fill"
                        style="width:{confidence_percent:.2f}%"
                    ></div>
                </div>

            </div>

            <div class="action-box">

                <div class="action-label">
                    Recommended action
                </div>

                <div class="action-value">
                    {safe_action}
                </div>

            </div>

        </div>
        """
    )

    if confidence >= 0.90:
        st.success(
            "High-confidence prediction"
        )
    elif confidence >= 0.70:
        st.warning(
            "Moderate-confidence prediction. A clearer image may improve reliability."
        )
    else:
        st.error(
            "Low-confidence prediction. Try another image with the material clearly visible."
        )


st.html(
    """
    <div class="section-title">
        Prediction overview
    </div>
    """
)


c1, c2, c3 = st.columns(
    3,
    gap="medium",
)


impact = sustainability.get(
    "impact",
    "Not available",
)

recyclability = sustainability.get(
    "recyclability",
    "Not available",
)

category = sustainability.get(
    "category",
    "Waste material",
)


with c1:
    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-icon">
                🎯
            </div>

            <div class="metric-title">
                Confidence
            </div>

            <div class="metric-value">
                {confidence_percent:.2f}%
            </div>

        </div>
        """
    )


with c2:
    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-icon">
                🌱
            </div>

            <div class="metric-title">
                Environmental Impact
            </div>

            <div class="metric-value">
                {html.escape(str(impact))}
            </div>

        </div>
        """
    )


with c3:
    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-icon">
                ♻️
            </div>

            <div class="metric-title">
                Recovery
            </div>

            <div class="metric-value">
                {html.escape(str(recyclability))}
            </div>

        </div>
        """
    )


st.html(
    """
    <div class="section-title">
        🔎 Top predictions
    </div>

    <div class="section-subtitle">
        The three most likely waste categories identified by EcoSort AI.
    </div>
    """
)


for rank, index in enumerate(
    top_indices[:3],
    start=1,
):
    probability = float(
        predictions[index]
    )

    prediction_name = class_names[
        int(index)
    ]

    probability_percent = probability * 100

    st.html(
        f"""
        <div class="prediction-card">

            <div class="prediction-row">

                <div class="prediction-name">
                    #{rank} {html.escape(str(prediction_name))}
                </div>

                <div class="prediction-score">
                    {probability_percent:.2f}%
                </div>

            </div>

        </div>
        """
    )

    st.progress(
        probability
    )


st.html(
    """
    <div class="section-title">
        🌍 Sustainability profile
    </div>
    """
)


c1, c2, c3 = st.columns(
    3,
    gap="medium",
)


with c1:
    st.html(
        f"""
        <div class="profile-card">

            <div class="profile-label">
                Impact level
            </div>

            <div class="profile-value">
                🌱 {html.escape(str(impact))}
            </div>

        </div>
        """
    )


with c2:
    st.html(
        f"""
        <div class="profile-card">

            <div class="profile-label">
                Material category
            </div>

            <div class="profile-value">
                🏷️ {html.escape(str(category))}
            </div>

        </div>
        """
    )


with c3:
    st.html(
        f"""
        <div class="profile-card">

            <div class="profile-label">
                Recyclability
            </div>

            <div class="profile-value">
                ♻️ {html.escape(str(recyclability))}
            </div>

        </div>
        """
    )


description = sustainability.get(
    "description",
    "Sustainability information is not available for this category.",
)


st.html(
    f"""
    <div class="description-card">

        <strong style="color:#e3f3e7;">
            About {safe_display_name}
        </strong>

        <br><br>

        {html.escape(str(description))}

    </div>
    """
)


carbon = sustainability.get(
    "carbon",
    "Carbon information is not available for this category.",
)


st.html(
    """
    <div class="section-title">
        🌱 Carbon footprint awareness
    </div>
    """
)


st.html(
    f"""
    <div class="carbon-card">

        <div class="carbon-title">
            ♻️ Environmental perspective
        </div>

        <div class="carbon-text">
            {html.escape(str(carbon))}
        </div>

    </div>
    """
)


st.caption(
    "This is a comparative sustainability indicator, not a product-level life-cycle carbon calculation."
)


st.html(
    """
    <div class="section-title">
        💡 What should you do?
    </div>
    """
)


tips = sustainability.get(
    "tips",
    [],
)


for tip in tips:
    st.html(
        f"""
        <div class="tip-card">
            ✓ &nbsp; {html.escape(str(tip))}
        </div>
        """
    )


st.html(
    """
    <div class="section-title">
        🎯 Related Sustainable Development Goals
    </div>

    <div class="section-subtitle">
        Relevant SDGs associated with this waste category.
    </div>
    """
)


sdg_info = {
    "SDG 3": (
        "Good Health & Well-Being",
        ["3.png", "3.jpg", "3.jpeg"],
    ),
    "SDG 6": (
        "Clean Water & Sanitation",
        ["6.png", "6.jpg", "6.jpeg"],
    ),
    "SDG 7": (
        "Affordable & Clean Energy",
        ["7.png", "7.jpg", "7.jpeg"],
    ),
    "SDG 12": (
        "Responsible Consumption",
        ["12.png", "12.jpg", "12.jpeg"],
    ),
    "SDG 13": (
        "Climate Action",
        ["13.png", "13.jpg", "13.jpeg"],
    ),
    "SDG 14": (
        "Life Below Water",
        ["14.png", "14.jpg", "14.jpeg"],
    ),
    "SDG 15": (
        "Life on Land",
        ["15.png", "15.jpg", "15.jpeg"],
    ),
}


sdgs = sustainability.get(
    "sdgs",
    [],
)


if sdgs:
    sdg_columns = st.columns(
        len(sdgs),
        gap="medium",
    )

    for column, sdg in zip(
        sdg_columns,
        sdgs,
    ):
        with column:
            title, filenames = sdg_info.get(
                sdg,
                (
                    sdg,
                    [],
                ),
            )

            image_path = next(
                (
                    ASSETS_DIR / filename
                    for filename in filenames
                    if (
                        ASSETS_DIR / filename
                    ).exists()
                ),
                None,
            )

            safe_sdg = html.escape(
                str(sdg)
            )

            safe_title = html.escape(
                str(title)
            )

            if image_path:
                image_data = base64.b64encode(
                    image_path.read_bytes()
                ).decode("utf-8")

                mime_type = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                }.get(
                    image_path.suffix.lower(),
                    "image/png",
                )

                st.html(
                    f"""
                    <div class="sdg-card">

                        <img
                            class="sdg-image"
                            src="data:{mime_type};base64,{image_data}"
                            alt="{safe_sdg}"
                        >

                        <div class="sdg-name">
                            {safe_sdg}
                        </div>

                        <div class="sdg-description">
                            {safe_title}
                        </div>

                    </div>
                    """
                )

            else:
                st.html(
                    f"""
                    <div class="sdg-card">

                        <div style="
                            height:125px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            color:#718d78;
                            font-weight:800;
                            font-size:1.1rem;
                        ">
                            {safe_sdg}
                        </div>

                        <div class="sdg-name">
                            {safe_sdg}
                        </div>

                        <div class="sdg-description">
                            {safe_title}
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
        AI-assisted waste classification · Sustainability awareness ·
        Responsible waste management
    </div>
    """
)