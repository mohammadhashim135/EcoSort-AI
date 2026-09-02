import base64
import html
from pathlib import Path

import streamlit as st

from sustainability import (
    SUSTAINABILITY_DATA,
    get_sustainability_data,
)


BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"


st.set_page_config(
    page_title="Sustainability | EcoSort AI",
    page_icon="🌱",
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
                circle at 8% 5%,
                rgba(53, 180, 91, 0.11),
                transparent 30%
            ),
            radial-gradient(
                circle at 92% 20%,
                rgba(53, 160, 83, 0.07),
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
        width: 320px;
        height: 320px;
        right: -100px;
        top: -140px;
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

    .sidebar-card {
        padding: 1rem;
        border-radius: 16px;
        background: rgba(65, 181, 91, 0.08);
        border: 1px solid rgba(91, 198, 111, 0.15);
        color: #a8c9ae;
        font-size: 0.82rem;
        line-height: 1.65;
    }

    .selector-card {
        padding: 1.6rem 1.8rem;
        border-radius: 24px;
        background:
            linear-gradient(
                145deg,
                rgba(17, 48, 29, 0.97),
                rgba(7, 27, 16, 0.97)
            );
        border: 1px solid rgba(103, 184, 122, 0.18);
        margin-bottom: 2rem;
    }

    .selector-title {
        color: #effbf2;
        font-size: 1.15rem;
        font-weight: 850;
    }

    .selector-text {
        color: #87a58f;
        margin-top: 0.4rem;
        font-size: 0.88rem;
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

    .overview-card {
        padding: 2.3rem;
        border-radius: 27px;
        background:
            linear-gradient(
                145deg,
                rgba(16, 62, 36, 0.98),
                rgba(7, 28, 17, 0.98)
            );
        border: 1px solid rgba(102, 196, 122, 0.20);
        min-height: 350px;
        box-sizing: border-box;
        box-shadow: 0 20px 55px rgba(0, 0, 0, 0.14);
    }

    .material-icon {
        font-size: 3rem;
        margin-bottom: 1.2rem;
    }

    .material-label {
        color: #83a68d;
        font-size: 0.73rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-weight: 850;
    }

    .material-name {
        color: #f0fff3;
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: -0.055em;
        margin-top: 0.3rem;
    }

    .material-description {
        color: #a5c3ac;
        font-size: 1rem;
        line-height: 1.8;
        margin-top: 1rem;
        max-width: 700px;
    }

    .score-card {
        padding: 2.4rem;
        border-radius: 27px;
        background:
            linear-gradient(
                145deg,
                rgba(14, 48, 27, 0.98),
                rgba(6, 24, 14, 0.98)
            );
        border: 1px solid rgba(103, 184, 122, 0.18);
        min-height: 350px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
    }

    .score-circle {
        width: 205px;
        height: 205px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background:
            conic-gradient(
                #68d981 0deg,
                #68d981 var(--score-degree),
                rgba(102, 151, 111, 0.18) var(--score-degree),
                rgba(102, 151, 111, 0.18) 360deg
            );
        position: relative;
    }

    .score-circle::before {
        content: "";
        position: absolute;
        inset: 15px;
        border-radius: 50%;
        background: #081b10;
    }

    .score-number {
        position: relative;
        z-index: 2;
        color: #effff2;
        font-size: 2.9rem;
        font-weight: 900;
        letter-spacing: -0.06em;
    }

    .score-label {
        color: #789883;
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 850;
        margin-top: 1.4rem;
        text-align: center;
    }

    .info-card {
        padding: 1.7rem;
        border-radius: 23px;
        background:
            linear-gradient(
                145deg,
                rgba(16, 43, 26, 0.97),
                rgba(8, 25, 16, 0.97)
            );
        border: 1px solid rgba(100, 163, 115, 0.15);
        min-height: 210px;
        box-sizing: border-box;
    }

    .info-icon {
        font-size: 1.8rem;
        margin-bottom: 0.8rem;
    }

    .info-label {
        color: #789883;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        font-weight: 850;
    }

    .info-value {
        color: #eaf8ed;
        font-size: 1.25rem;
        font-weight: 850;
        margin-top: 0.35rem;
    }

    .info-text {
        color: #91aa97;
        line-height: 1.65;
        font-size: 0.84rem;
        margin-top: 0.45rem;
    }

    .action-card {
        padding: 2rem;
        border-radius: 25px;
        background:
            linear-gradient(
                135deg,
                rgba(22, 68, 39, 0.96),
                rgba(8, 29, 17, 0.98)
            );
        border: 1px solid rgba(105, 196, 123, 0.20);
    }

    .action-title {
        color: #effff2;
        font-size: 1.45rem;
        font-weight: 900;
    }

    .action-text {
        color: #a2c0aa;
        line-height: 1.75;
        margin-top: 0.65rem;
    }

    .impact-card {
        padding: 2rem;
        border-radius: 25px;
        background:
            linear-gradient(
                145deg,
                rgba(16, 43, 26, 0.97),
                rgba(8, 25, 16, 0.97)
            );
        border: 1px solid rgba(100, 163, 115, 0.15);
    }

    .impact-title {
        color: #effbf2;
        font-size: 1.25rem;
        font-weight: 850;
    }

    .impact-text {
        color: #93ad99;
        line-height: 1.75;
        margin-top: 0.7rem;
        font-size: 0.88rem;
    }

    .tip-card {
        padding: 1.35rem;
        border-radius: 20px;
        background: rgba(12, 37, 22, 0.92);
        border: 1px solid rgba(91, 160, 106, 0.14);
        min-height: 150px;
        box-sizing: border-box;
    }

    .tip-icon {
        font-size: 1.5rem;
    }

    .tip-title {
        color: #eaf8ed;
        font-size: 0.95rem;
        font-weight: 850;
        margin-top: 0.55rem;
    }

    .tip-text {
        color: #849f8b;
        font-size: 0.8rem;
        line-height: 1.6;
        margin-top: 0.35rem;
    }

    .sdg-card {
        padding: 1rem;
        border-radius: 20px;
        background:
            linear-gradient(
                145deg,
                rgba(15, 42, 25, 0.96),
                rgba(7, 24, 14, 0.96)
            );
        border: 1px solid rgba(100, 163, 115, 0.14);
        text-align: center;
        height: 100%;
        box-sizing: border-box;
    }

    .sdg-image {
        width: 100%;
        max-width: 120px;
        height: 120px;
        object-fit: contain;
        border-radius: 14px;
        margin: 0 auto 0.8rem auto;
        display: block;
    }

    .sdg-name {
        color: #e9f8ec;
        font-size: 0.82rem;
        font-weight: 850;
    }

    .category-card {
        padding: 1rem 1.25rem;
        border-radius: 18px;
        background:
            linear-gradient(
                145deg,
                rgba(11, 35, 21, 0.96),
                rgba(7, 25, 15, 0.96)
            );
        border: 1px solid rgba(91, 157, 106, 0.13);
        margin-bottom: 0.8rem;
    }

    .category-name {
        color: #e7f5ea;
        font-weight: 850;
    }

    .category-impact {
        color: #72dc8b;
        float: right;
        font-weight: 750;
        font-size: 0.82rem;
    }

    .disclaimer {
        padding: 1.2rem 1.4rem;
        border-radius: 18px;
        background: rgba(24, 52, 32, 0.78);
        border: 1px solid rgba(104, 174, 119, 0.15);
        color: #91aa97;
        line-height: 1.7;
        font-size: 0.82rem;
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
                Sustainability Intelligence
            </div>

        </div>
        """
    )

    st.html(
        """
        <div class="sidebar-card">
            Explore the environmental characteristics,
            recommended recovery actions, and Sustainable
            Development Goal connections for each waste category.
        </div>
        """
    )

    st.html(
        """
        <div class="sidebar-card" style="margin-top:1rem;">
            <strong style="color:#a8e6b3;">
                9 Categories
            </strong>
            <br>
            Aluminium · Carton · E-waste · Glass · Organic Waste
            · Paper & Cardboard · Plastics · Textiles · Wood
        </div>
        """
    )


st.html(
    """
    <div class="hero">

        <div class="badge">
            🌱 ECO SORT AI · SUSTAINABILITY INTELLIGENCE
        </div>

        <h1 class="hero-title">
            Understand the <span>impact.</span>
        </h1>

        <div class="hero-text">
            Explore sustainability information for every waste
            category recognized by EcoSort AI and understand the
            recommended recovery pathway for each material.
        </div>

    </div>
    """
)


st.html(
    """
    <div class="selector-card">

        <div class="selector-title">
            ♻️ Material selector
        </div>

        <div class="selector-text">
            Choose one of the nine categories supported by the EcoSort AI model.
        </div>

    </div>
    """
)


class_names = list(SUSTAINABILITY_DATA.keys())


selected_material = st.selectbox(
    "Select waste category",
    class_names,
    label_visibility="collapsed",
)


data = get_sustainability_data(
    selected_material
)


material_name = selected_material.replace(
    "_",
    " & ",
) if selected_material == "Paper_and_Cardboard" else selected_material.replace(
    "_",
    " ",
)


impact_level = data.get(
    "impact_level",
    data.get(
        "impact",
        "Not specified",
    ),
)


score = data.get(
    "score",
    data.get(
        "impact_score",
        0,
    ),
)


try:
    score = float(score)
except (
    TypeError,
    ValueError,
):
    score = 0


score = max(
    0,
    min(
        5,
        score,
    ),
)


score_degree = score / 5 * 360


description = data.get(
    "description",
    data.get(
        "summary",
        "Sustainability information is available for this material.",
    ),
)


recyclability = data.get(
    "recyclability",
    "Not specified",
)


recommended_action = data.get(
    "recommended_action",
    data.get(
        "action",
        "Follow local waste-management guidance.",
    ),
)


material_type = data.get(
    "material_type",
    data.get(
        "type",
        "Waste material",
    ),
)


st.html(
    '<div class="section-title">🌍 Sustainability Overview</div>'
)

st.html(
    """
    <div class="section-subtitle">
        Environmental characteristics and recommended recovery pathway for the selected material.
    </div>
    """
)


c1, c2 = st.columns(
    [1.35, 1],
    gap="large",
)


with c1:

    st.html(
        f"""
        <div class="overview-card">

            <div class="material-icon">
                ♻️
            </div>

            <div class="material-label">
                Selected Material
            </div>

            <div class="material-name">
                {html.escape(material_name)}
            </div>

            <div class="material-description">
                {html.escape(str(description))}
            </div>

        </div>
        """
    )


with c2:

    st.html(
        f"""
        <div class="score-card">

            <div
                class="score-circle"
                style="--score-degree:{score_degree}deg;"
            >

                <div class="score-number">
                    {score:g}/5
                </div>

            </div>

            <div class="score-label">
                Environmental Impact Score
            </div>

        </div>
        """
    )


st.html(
    '<div class="section-title">📊 Material Profile</div>'
)

st.html(
    """
    <div class="section-subtitle">
        Key sustainability characteristics of the selected waste category.
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
        <div class="info-card">

            <div class="info-icon">
                🌎
            </div>

            <div class="info-label">
                Environmental Impact
            </div>

            <div class="info-value">
                {html.escape(str(impact_level))}
            </div>

            <div class="info-text">
                Relative environmental impact classification
                associated with this material.
            </div>

        </div>
        """
    )


with c2:

    st.html(
        f"""
        <div class="info-card">

            <div class="info-icon">
                🔄
            </div>

            <div class="info-label">
                Recyclability
            </div>

            <div class="info-value">
                {html.escape(str(recyclability))}
            </div>

            <div class="info-text">
                Indicates the potential for effective material recovery through proper waste management.               
            </div>

        </div>
        """
    )


with c3:

    st.html(
        f"""
        <div class="info-card">

            <div class="info-icon">
                🧱
            </div>

            <div class="info-label">
                Material Profile
            </div>

            <div class="info-value">
                {html.escape(str(material_type))}
            </div>

            <div class="info-text">
                General material grouping used by EcoSort AI
                sustainability information.
            </div>

        </div>
        """
    )


st.html(
    '<div class="section-title">♻️ Recommended Recovery Action</div>'
)

st.html(
    """
    <div class="section-subtitle">
        Practical guidance for handling the selected material.
    </div>
    """
)


st.html(
    f"""
    <div class="action-card">

        <div class="action-title">
            {html.escape(str(recommended_action))}
        </div>

        <div class="action-text">
            Choose the appropriate recovery route based on local
            recycling and waste-management rules. Material condition,
            contamination, and local collection systems can affect
            the correct disposal pathway.
        </div>

    </div>
    """
)


st.html(
    '<div class="section-title">🌱 Sustainability Awareness</div>'
)

st.html(
    """
    <div class="section-subtitle">
        Why responsible handling of this material matters.
    </div>
    """
)


awareness_text = {
    "Aluminium": (
        "Recovering aluminium can reduce the need for new raw-material "
        "extraction because the material can be recycled repeatedly."
    ),
    "Carton": (
        "Clean carton can often enter paper-based recovery streams, "
        "helping retain useful fibre and reduce disposal."
    ),
    "E-waste": (
        "Electronic waste may contain recoverable materials as well as "
        "components requiring specialized handling."
    ),
    "Glass": (
        "Glass can be recovered and recycled through suitable collection "
        "systems, helping retain material value."
    ),
    "Organic_Waste": (
        "Organic waste can often be diverted from disposal through "
        "composting or other biological treatment pathways."
    ),
    "Paper_and_Cardboard": (
        "Clean and dry paper and cardboard can often be recovered into "
        "new paper products through established recycling systems."
    ),
    "Plastics": (
        "Plastic recovery depends strongly on polymer type, contamination, "
        "and the recycling infrastructure available locally."
    ),
    "Textiles": (
        "Extending textile life through reuse, repair, donation, or "
        "specialized textile recovery can reduce unnecessary disposal."
    ),
    "Wood": (
        "Wood materials may be suitable for reuse, repair, recovery, "
        "or other pathways depending on treatment and contamination."
    ),
}


st.html(
    f"""
    <div class="impact-card">

        <div class="impact-title">
            Environmental Perspective
        </div>

        <div class="impact-text">
            {html.escape(
                awareness_text.get(
                    selected_material,
                    "Responsible recovery can help conserve resources and reduce waste sent to disposal."
                )
            )}
        </div>

    </div>
    """
)


st.html(
    '<div class="section-title">💡 Practical Guidance</div>'
)

st.html(
    """
    <div class="section-subtitle">
        Simple actions that improve waste recovery outcomes.
    </div>
    """
)


tips = [
    (
        "🧼",
        "Keep recyclables clean",
        "Remove food residue and unnecessary contamination where appropriate."
    ),
    (
        "📦",
        "Sort correctly",
        "Keep different material categories separated when local systems require it."
    ),
    (
        "🏠",
        "Check local rules",
        "Accepted materials and collection methods may vary between different locations."
    ),
    (
        "♻️",
        "Prefer recovery",
        "Reuse, repair, recycling, or composting can be preferable to disposal when available."
    ),
]


tip_columns = st.columns(
    4,
    gap="medium",
)


for column, tip in zip(
    tip_columns,
    tips,
):

    with column:

        st.html(
            f"""
            <div class="tip-card">

                <div class="tip-icon">
                    {tip[0]}
                </div>

                <div class="tip-title">
                    {html.escape(tip[1])}
                </div>

                <div class="tip-text">
                    {html.escape(tip[2])}
                </div>

            </div>
            """
        )


sdgs = data.get(
    "sdgs",
    [],
)


if sdgs:

    st.html(
        '<div class="section-title">🌐 Related Sustainable Development Goals</div>'
    )

    st.html(
        """
        <div class="section-subtitle">
            Sustainability goals contextually connected to responsible material management.
        </div>
        """
    )

    sdg_columns = st.columns(
        min(
            len(sdgs),
            4,
        ),
        gap="medium",
    )

    sdg_images = data.get(
        "sdg_images",
        {},
    )

    for index, sdg in enumerate(sdgs):

        column = sdg_columns[
            index % len(sdg_columns)
        ]

        image_name = sdg_images.get(
            sdg
        )

        with column:

            if image_name:

                image_path = (
                    ASSETS_DIR /
                    image_name
                )

                if image_path.exists():

                    with open(
                        image_path,
                        "rb",
                    ) as file:

                        image_base64 = base64.b64encode(
                            file.read()
                        ).decode(
                            "utf-8"
                        )

                    extension = image_path.suffix.lower().replace(
                        ".",
                        "",
                    )

                    if extension == "jpg":
                        extension = "jpeg"

                    st.html(
                        f"""
                        <div class="sdg-card">

                            <img
                                class="sdg-image"
                                src="data:image/{extension};base64,{image_base64}"
                            >

                            <div class="sdg-name">
                                {html.escape(str(sdg))}
                            </div>

                        </div>
                        """
                    )

                    continue

            st.html(
                f"""
                <div class="sdg-card">

                    <div style="
                        font-size:3rem;
                        padding:2rem 0;
                    ">
                        🌍
                    </div>

                    <div class="sdg-name">
                        {html.escape(str(sdg))}
                    </div>

                </div>
                """
            )


st.html(
    '<div class="section-title">🗂️ All Waste Categories</div>'
)

st.html(
    """
    <div class="section-subtitle">
        Quick sustainability reference for all categories supported by EcoSort AI.
    </div>
    """
)


for category, category_data in SUSTAINABILITY_DATA.items():

    category_name = category.replace(
        "_",
        " ",
    )

    if category == "Paper_and_Cardboard":

        category_name = "Paper & Cardboard"

    category_impact = category_data.get(
        "impact_level",
        category_data.get(
            "impact",
            "Not specified",
        ),
    )

    st.html(
        f"""
        <div class="category-card">

            <span class="category-name">
                ♻️ {html.escape(category_name)}
            </span>

            <span class="category-impact">
                {html.escape(str(category_impact))}
            </span>

        </div>
        """
    )


st.html(
    """
    <div class="disclaimer">

        <strong style="color:#a8c7af;">
            Sustainability note
        </strong>

        <br>

        The environmental impact scores shown here are category-level
        sustainability indicators used by EcoSort AI. They are not
        direct measurements of carbon emissions or lifecycle impacts.
        Actual environmental outcomes depend on material composition,
        contamination, collection systems, transport, processing,
        recycling infrastructure, and local waste-management practices.

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

        Intelligent Waste Classification · Sustainability Intelligence ·
        Responsible Resource Recovery

    </div>
    """
)