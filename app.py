from pathlib import Path
import base64
import json

import streamlit as st


st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
ASSETS_DIR = BASE_DIR / "assets"
METRICS_PATH = MODEL_DIR / "metrics.json"


metrics = {
    "accuracy": 0.9296,
    "precision": 0.9300,
    "recall": 0.9296,
    "f1_score": 0.9297,
}


if METRICS_PATH.exists():
    try:
        with open(METRICS_PATH, "r", encoding="utf-8") as file:
            saved_metrics = json.load(file)
        metrics.update(saved_metrics)
    except (OSError, json.JSONDecodeError):
        pass


accuracy = float(metrics.get("accuracy", 0.9296)) * 100
precision = float(metrics.get("precision", 0.9300)) * 100
recall = float(metrics.get("recall", 0.9296)) * 100
f1_score = float(metrics.get("f1_score", 0.9297)) * 100


TOTAL_IMAGES = 8235
TRAINING_IMAGES = 6588
VALIDATION_IMAGES = 1647
NUM_CLASSES = 9
IMAGE_SIZE = "224 × 224"
TOTAL_EPOCHS = 20
MODEL_NAME = "EfficientNetB0"
HARDWARE = "NVIDIA Tesla T4"


st.html(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(38, 166, 91, 0.13),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(46, 125, 50, 0.10),
                transparent 25%
            ),
            #07110c;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Keep Streamlit's sidebar expand/collapse button visible */
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        z-index: 999999 !important;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #08150e 0%,
                #0b1c13 100%
            );
        border-right: 1px solid rgba(98, 160, 117, 0.16);
    }

    [data-testid="stSidebar"] * {
        color: #e7f4eb;
    }

    .brand {
        padding: 0.5rem 0 1.5rem 0;
    }

    .brand-title {
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .brand-subtitle {
        color: #8fb59c;
        font-size: 0.82rem;
        margin-top: 0.2rem;
    }

    .sidebar-section {
        color: #6f8d79;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-weight: 800;
        margin-bottom: 0.7rem;
    }

    .sidebar-note {
        color: #8da895;
        font-size: 0.82rem;
        line-height: 1.55;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 4.2rem 4rem;
        border-radius: 32px;
        background:
            linear-gradient(
                135deg,
                rgba(17, 59, 39, 0.98),
                rgba(7, 25, 16, 0.98)
            );
        border: 1px solid rgba(92, 168, 116, 0.25);
        box-shadow:
            0 25px 80px rgba(0, 0, 0, 0.30),
            inset 0 1px 0 rgba(255, 255, 255, 0.04);
        margin-bottom: 2rem;
    }

    .hero::before {
        content: "";
        position: absolute;
        width: 360px;
        height: 360px;
        border-radius: 50%;
        right: -130px;
        top: -170px;
        background: rgba(76, 175, 80, 0.12);
        filter: blur(4px);
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        left: 45%;
        bottom: -170px;
        background: rgba(129, 199, 132, 0.08);
    }

    .hero-content {
        position: relative;
        z-index: 2;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        background: rgba(111, 201, 134, 0.12);
        border: 1px solid rgba(111, 201, 134, 0.25);
        color: #a9e5b8;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: clamp(2.8rem, 6vw, 5.4rem);
        line-height: 0.98;
        font-weight: 900;
        letter-spacing: -0.065em;
        margin: 0;
        color: #f2fff5;
    }

    .hero-title span {
        color: #72d98b;
    }

    .hero-description {
        max-width: 760px;
        color: #b8d3c0;
        font-size: 1.16rem;
        line-height: 1.7;
        margin-top: 1.4rem;
    }

    .hero-flow {
        margin-top: 1.8rem;
        color: #e4f4e8;
        font-weight: 700;
        font-size: 1rem;
    }

    .section-title {
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        color: #eefaf1;
        margin-top: 2.5rem;
        margin-bottom: 1rem;
    }

    .section-subtitle {
        color: #8eaa98;
        margin-top: -0.6rem;
        margin-bottom: 1.5rem;
    }

    .feature {
        height: 100%;
        min-height: 230px;
        padding: 1.7rem;
        border-radius: 24px;
        background:
            linear-gradient(
                145deg,
                rgba(19, 43, 29, 0.94),
                rgba(10, 27, 18, 0.94)
            );
        border: 1px solid rgba(101, 156, 117, 0.17);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.16);
    }

    .feature-icon {
        width: 52px;
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        background: rgba(89, 190, 112, 0.12);
        border: 1px solid rgba(89, 190, 112, 0.18);
        font-size: 1.45rem;
        margin-bottom: 1.2rem;
    }

    .feature-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #edf9f0;
        margin-bottom: 0.7rem;
    }

    .feature-text {
        color: #91ad9a;
        line-height: 1.65;
        font-size: 0.95rem;
    }

    .stat {
        height: 100%;
        min-height: 145px;
        padding: 1.5rem 1rem;
        border-radius: 22px;
        text-align: center;
        background:
            linear-gradient(
                145deg,
                rgba(18, 43, 28, 0.96),
                rgba(9, 25, 16, 0.96)
            );
        border: 1px solid rgba(105, 168, 119, 0.18);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.14);
    }

    .stat-number {
        color: #7ce393;
        font-size: 2.05rem;
        font-weight: 900;
        letter-spacing: -0.04em;
    }

    .stat-label {
        color: #8fa998;
        font-size: 0.76rem;
        margin-top: 0.45rem;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        font-weight: 700;
    }

    .model-card {
        height: 100%;
        padding: 1.8rem;
        border-radius: 26px;
        background:
            linear-gradient(
                135deg,
                rgba(14, 39, 25, 0.96),
                rgba(8, 24, 15, 0.96)
            );
        border: 1px solid rgba(99, 163, 115, 0.18);
    }

    .model-title {
        color: #effbf2;
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 0.6rem;
    }

    .model-text {
        color: #91aa98;
        line-height: 1.65;
        font-size: 0.93rem;
    }

    .model-pill {
        display: inline-block;
        margin-top: 1rem;
        margin-right: 0.4rem;
        padding: 0.42rem 0.7rem;
        border-radius: 999px;
        background: rgba(105, 190, 122, 0.10);
        border: 1px solid rgba(105, 190, 122, 0.18);
        color: #a5dfb2;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .performance-card {
        height: 100%;
        padding: 1.8rem;
        border-radius: 26px;
        background:
            linear-gradient(
                145deg,
                rgba(18, 43, 28, 0.96),
                rgba(8, 25, 16, 0.96)
            );
        border: 1px solid rgba(101, 165, 116, 0.17);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.14);
    }

    .performance-icon {
        font-size: 1.5rem;
        margin-bottom: 0.8rem;
    }

    .performance-title {
        color: #eefaf1;
        font-size: 1.05rem;
        font-weight: 800;
    }

    .performance-value {
        color: #7ce393;
        font-size: 2rem;
        font-weight: 900;
        margin-top: 0.5rem;
    }

    .performance-text {
        color: #8da895;
        font-size: 0.84rem;
        line-height: 1.55;
        margin-top: 0.4rem;
    }

    .sdg-card {
        min-height: 285px;
        padding: 1rem;
        border-radius: 22px;
        background:
            linear-gradient(
                145deg,
                rgba(12, 36, 23, 0.96),
                rgba(7, 25, 16, 0.96)
            );
        border: 1px solid rgba(101, 156, 117, 0.16);
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.14);
    }

    .sdg-image {
        width: 100%;
        height: 150px;
        object-fit: contain;
        border-radius: 14px;
        display: block;
        margin: 0 auto;
    }

    .sdg-label {
        color: #d5e8da;
        font-size: 0.88rem;
        font-weight: 800;
        margin-top: 0.8rem;
    }

    .sdg-description {
        color: #91aa98;
        font-size: 0.78rem;
        line-height: 1.45;
        margin-top: 0.4rem;
    }

    .cta {
        padding: 2.2rem;
        border-radius: 26px;
        background:
            linear-gradient(
                135deg,
                rgba(31, 89, 51, 0.55),
                rgba(10, 36, 21, 0.72)
            );
        border: 1px solid rgba(110, 205, 132, 0.22);
        text-align: center;
        margin-top: 2.5rem;
    }

    .cta-title {
        color: #f0fff3;
        font-size: 1.5rem;
        font-weight: 800;
    }

    .cta-text {
        color: #a2c1ac;
        margin-top: 0.45rem;
    }

    .footer {
        text-align: center;
        color: #627c6b;
        font-size: 0.78rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(100, 150, 110, 0.10);
    }

    @media (max-width: 900px) {
        .hero {
            padding: 3rem 2rem;
            border-radius: 26px;
        }

        .hero-title {
            font-size: 3.2rem;
        }
    }

    </style>
    """
)


with st.sidebar:
    st.html(
        """
        <div class="brand">
            <div class="brand-title">♻️ EcoSort AI</div>
            <div class="brand-subtitle">
                AI-powered waste intelligence
            </div>
        </div>
        """
    )

    st.divider()

    st.html(
        """
        <div class="sidebar-section">
            Project
        </div>
        """
    )

    st.caption(
        "Explore waste classification, sustainability insights, "
        "and model performance."
    )

    st.divider()

    st.html(
        """
        <div class="sidebar-section">
            Model performance
        </div>
        """
    )

    st.html(
        f"""
        <div style="
            padding: 1rem;
            border-radius: 16px;
            background: rgba(70, 150, 88, 0.08);
            border: 1px solid rgba(100, 170, 115, 0.12);
        ">
            <div style="
                color:#78dc8e;
                font-size:1.45rem;
                font-weight:800;
            ">
                {accuracy:.2f}%
            </div>
            <div style="
                color:#88a792;
                font-size:0.78rem;
                margin-top:0.2rem;
            ">
                Validation Accuracy
            </div>
        </div>
        """
    )

    st.divider()

    st.html(
        f"""
        <div class="sidebar-note">
            <b>{MODEL_NAME}</b><br>
            {NUM_CLASSES}-class classification<br>
            {IMAGE_SIZE} input<br>
            {TOTAL_EPOCHS} maximum epochs
        </div>
        """
    )


st.html(
    """
    <div class="hero">
        <div class="hero-content">

            <div class="hero-badge">
                🌱 Intelligent Waste Classification
            </div>

            <h1 class="hero-title">
                Waste smarter.<br>
                Live <span>greener.</span>
            </h1>

            <div class="hero-description">
                EcoSort AI transforms a simple waste image into an
                intelligent classification, sustainability profile,
                disposal recommendation, and environmental insight.
            </div>

            <div class="hero-flow">
                📷 Classify &nbsp;→&nbsp;
                🌍 Understand &nbsp;→&nbsp;
                ♻️ Act &nbsp;→&nbsp;
                🌱 Impact
            </div>

        </div>
    </div>
    """
)


st.html(
    """
    <div class="section-title">
        What EcoSort AI does
    </div>

    <div class="section-subtitle">
        From image recognition to meaningful environmental action.
    </div>
    """
)


c1, c2, c3 = st.columns(3, gap="large")


with c1:
    st.html(
        """
        <div class="feature">
            <div class="feature-icon">📷</div>
            <div class="feature-title">
                AI Waste Classification
            </div>
            <div class="feature-text">
                Upload a waste image and the EfficientNetB0
                computer-vision model identifies the most likely
                waste category across nine classes.
            </div>
        </div>
        """
    )


with c2:
    st.html(
        """
        <div class="feature">
            <div class="feature-icon">🌍</div>
            <div class="feature-title">
                Sustainability Intelligence
            </div>
            <div class="feature-text">
                Discover recyclability, environmental impact,
                recommended actions, and practical disposal tips
                for the detected material.
            </div>
        </div>
        """
    )


with c3:
    st.html(
        """
        <div class="feature">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">
                SDG Connection
            </div>
            <div class="feature-text">
                Connect everyday waste-management decisions with
                relevant United Nations Sustainable Development Goals.
            </div>
        </div>
        """
    )


st.html(
    """
    <div class="section-title">
        Model at a glance
    </div>

    <div class="section-subtitle">
        Key details from the final trained EcoSort AI model.
    </div>
    """
)


c1, c2, c3, c4 = st.columns(4, gap="medium")


stats = [
    (f"{TOTAL_IMAGES:,}", "Images Used"),
    (f"{TRAINING_IMAGES:,}", "Training Images"),
    (f"{VALIDATION_IMAGES:,}", "Validation Images"),
    (str(NUM_CLASSES), "Waste Classes"),
]


for column, (number, label) in zip(
    [c1, c2, c3, c4],
    stats,
):
    with column:
        st.html(
            f"""
            <div class="stat">
                <div class="stat-number">
                    {number}
                </div>
                <div class="stat-label">
                    {label}
                </div>
            </div>
            """
        )


st.html(
    """
    <div class="section-title">
        Final model configuration
    </div>

    <div class="section-subtitle">
        Transfer learning and fine-tuning configuration used for training.
    </div>
    """
)


c1, c2, c3, c4 = st.columns(4, gap="medium")


model_details = [
    (
        "🧠",
        "Architecture",
        "EfficientNetB0",
        "ImageNet pretrained",
    ),
    (
        "🖼️",
        "Input Resolution",
        "224 × 224",
        "RGB image input",
    ),
    (
        "⚙️",
        "Training",
        "20 Epochs",
        "8 initial + 12 fine-tuning",
    ),
    (
        "💻",
        "Hardware",
        "Tesla T4",
        "Google Colab GPU",
    ),
]


for column, (icon, title, value, text) in zip(
    [c1, c2, c3, c4],
    model_details,
):
    with column:
        st.html(
            f"""
            <div class="model-card">
                <div style="
                    font-size:1.5rem;
                    margin-bottom:0.7rem;
                ">
                    {icon}
                </div>

                <div class="model-title">
                    {title}
                </div>

                <div style="
                    color:#78dc8e;
                    font-size:1.35rem;
                    font-weight:900;
                    margin-top:0.35rem;
                ">
                    {value}
                </div>

                <div class="model-text" style="
                    margin-top:0.45rem;
                ">
                    {text}
                </div>
            </div>
            """
        )


st.html(
    """
    <div class="section-title">
        Model performance
    </div>

    <div class="section-subtitle">
        Validation performance on the held-out stratified validation set.
    </div>
    """
)


m1, m2, m3, m4 = st.columns(4, gap="medium")


performance = [
    (
        m1,
        "🎯",
        "Accuracy",
        accuracy,
        "Overall correct predictions",
    ),
    (
        m2,
        "📌",
        "Precision",
        precision,
        "Correct predicted classes",
    ),
    (
        m3,
        "🔎",
        "Recall",
        recall,
        "Identified actual classes",
    ),
    (
        m4,
        "🏆",
        "F1 Score",
        f1_score,
        "Precision recall balance",
    ),
]


for column, icon, title, value, text in performance:
    with column:
        st.html(
            f"""
            <div class="performance-card">
                <div class="performance-icon">
                    {icon}
                </div>

                <div class="performance-title">
                    {title}
                </div>

                <div class="performance-value">
                    {value:.2f}%
                </div>

                <div class="performance-text">
                    {text}
                </div>
            </div>
            """
        )


st.html(
    """
    <div class="section-title">
        Sustainable Development Goals
    </div>

    <div class="section-subtitle">
        Environmental action connected to global sustainability goals.
    </div>
    """
)


sdgs = [
    ("3", "Good Health & Well-Being"),
    ("6", "Clean Water & Sanitation"),
    ("12", "Responsible Consumption"),
    ("13", "Climate Action"),
    ("14", "Life Below Water"),
    ("15", "Life on Land"),
]


sdg_columns = st.columns(6, gap="medium")


for column, (number, label) in zip(sdg_columns, sdgs):
    image_candidates = [
        ASSETS_DIR / f"{number}.png",
        ASSETS_DIR / f"{number}.jpg",
        ASSETS_DIR / f"{number}.jpeg",
    ]

    image_path = next(
        (
            path
            for path in image_candidates
            if path.exists()
        ),
        None,
    )

    with column:
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
                        alt="SDG {number}"
                    >

                    <div class="sdg-label">
                        SDG {number}
                    </div>

                    <div class="sdg-description">
                        {label}
                    </div>
                </div>
                """
            )
        else:
            st.html(
                f"""
                <div class="sdg-card">
                    <div style="
                        height:150px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        color:#6f8c77;
                        font-weight:700;
                    ">
                        SDG {number}
                    </div>

                    <div class="sdg-label">
                        SDG {number}
                    </div>

                    <div class="sdg-description">
                        {label}
                    </div>
                </div>
                """
            )


st.html(
    """
    <div class="cta">
        <div class="cta-title">
            Ready to understand your waste?
        </div>

        <div class="cta-text">
            Choose <b>Classify Waste</b> from the navigation
            and upload an image to begin.
        </div>
    </div>
    """
)


st.html(
    """
    <div class="footer">
        EcoSort AI · Computer Vision for Sustainable Waste Management
        <p>
            Developed by
            <a
                href="https://github.com/mohammadhashim135"
                target="_blank"
            >
                Mohammad Hashim
            </a>
        </p>
    </div>
    """
)