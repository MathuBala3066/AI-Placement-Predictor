import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=st.secrets("GEMINI_API_KEY"))



import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Placement Scanner",
    page_icon="🚀",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------
model = joblib.load("placement_model.pkl")
model_columns = joblib.load("model_columns.pkl")

# ---------------- CYBERPUNK STYLING ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg: #0a0e14;
    --bg-panel: #10161f;
    --border: #1f2b3a;
    --accent: #00f0ff;
    --accent-violet: #a855f7;
    --success: #39ff88;
    --danger: #ff4566;
    --text-dim: #5a6b7d;
}

.stApp {
    background-color: var(--bg);
    background-image:
        radial-gradient(circle at 15% 20%, rgba(0, 240, 255, 0.05) 0%, transparent 35%),
        radial-gradient(circle at 85% 80%, rgba(168, 85, 247, 0.06) 0%, transparent 40%);
    color: #e6f1ff;
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Mono', monospace !important;
}

.eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.3em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 8px;
}

.eyebrow::before {
    content: '● ';
}

.subtitle {
    color: var(--text-dim);
    font-size: 14px;
    margin-bottom: 24px;
    line-height: 1.6;
}

.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.2em;
    color: var(--text-dim);
    text-transform: uppercase;
    margin-top: 24px;
    margin-bottom: 8px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}

/* Inputs */
.stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
    background-color: #0d1118 !important;
    border: 1px solid var(--border) !important;
    color: #e6f1ff !important;
    border-radius: 3px !important;
}

.stNumberInput label, .stSelectbox label {
    color: var(--text-dim) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

/* Button */
div.stButton > button {
    width: 100%;
    background: var(--accent);
    color: #04141a;
    border: none;
    border-radius: 3px;
    padding: 14px;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 20px;
    transition: all 0.15s ease;
}

div.stButton > button:hover {
    background: #5cf6ff;
    box-shadow: 0 0 24px rgba(0, 240, 255, 0.25);
    color: #04141a;
    border: none;
}

/* Result card */
.result-card {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 32px 24px;
    text-align: center;
    margin-top: 24px;
    position: relative;
    overflow: hidden;
}

.result-card.placed { border-top: 2px solid var(--success); }
.result-card.notplaced { border-top: 2px solid var(--danger); }

.status-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.3em;
    color: var(--text-dim);
    text-transform: uppercase;
    margin-bottom: 10px;
}

.status-title {
    font-family: 'Space Mono', monospace;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 12px;
}

.status-title.placed { color: var(--success); }
.status-title.notplaced { color: var(--danger); }

.status-desc {
    color: var(--text-dim);
    font-size: 14px;
    line-height: 1.7;
    max-width: 420px;
    margin: 0 auto 20px;
}

.stat-tags {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
}

.stat-tag {
    background: #0d1118;
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 8px 14px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.1em;
    color: var(--text-dim);
    text-transform: uppercase;
}

.stat-tag b {
    color: #e6f1ff;
}

.footer-note {
    text-align: center;
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 0.05em;
    margin-top: 24px;
    font-family: 'Space Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="eyebrow">System Online · ML Model v1</div>', unsafe_allow_html=True)
st.markdown("# Placement Scanner")
st.markdown(
    '<div class="subtitle">Enter your academic and skill profile below. '
    'The model analyzes 10 signals from your record and estimates your placement outcome.</div>',
    unsafe_allow_html=True
)

# ---------------- FORM ----------------
st.markdown('<div class="section-label">// Academic Record</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    cgpa = st.number_input("CGPA (0-10)", min_value=0.0, max_value=10.0, value=8.5, step=0.01)
    ssc = st.number_input("SSC Marks (%)", min_value=0, max_value=100, value=82)
with col2:
    aptitude = st.number_input("Aptitude Score (0-100)", min_value=0, max_value=100, value=78)
    hsc = st.number_input("HSC Marks (%)", min_value=0, max_value=100, value=80)

st.markdown('<div class="section-label">// Experience & Skills</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    internships = st.number_input("Internships (count)", min_value=0, value=1)
    certifications = st.number_input("Certifications (count)", min_value=0, value=2)
with col4:
    projects = st.number_input("Projects (count)", min_value=0, value=3)
    soft_skills = st.number_input("Soft Skills Rating (0-5)", min_value=0.0, max_value=5.0, value=4.2, step=0.1)

st.markdown('<div class="section-label">// Activity Flags</div>', unsafe_allow_html=True)
col5, col6 = st.columns(2)
with col5:
    extracurricular = st.selectbox("Extracurricular Activities", ["Yes", "No"])
with col6:
    placement_training = st.selectbox("Placement Training", ["Yes", "No"])

run_prediction = st.button("Run Prediction →")

# ---------------- PREDICTION ----------------
if run_prediction:
    input_data = {
        "CGPA": cgpa,
        "Internships": internships,
        "Projects": projects,
        "Workshops/Certifications": certifications,
        "AptitudeTestScore": aptitude,
        "SoftSkillsRating": soft_skills,
        "ExtracurricularActivities": 1 if extracurricular == "Yes" else 0,
        "PlacementTraining": 1 if placement_training == "Yes" else 0,
        "SSC_Marks": ssc,
        "HSC_Marks": hsc,
    }

    input_df = pd.DataFrame([input_data])
    input_df = input_df[model_columns]

    prediction = model.predict(input_df)[0]
    prob_placed = model.predict_proba(input_df)[0][1]

    is_placed = prediction == 1
    confidence = prob_placed if is_placed else (1 - prob_placed)
    confidence_pct = round(float(confidence) * 100, 2)
    placement_chance_pct = round(float(prob_placed) * 100, 2)

    status_class = "placed" if is_placed else "notplaced"
    status_label = "Placed" if is_placed else "Not Placed"
    status_title = "Placement Likely" if is_placed else "Placement Unlikely"
    status_desc = (
        "Your profile aligns closely with candidates who secured placements. "
        "Keep refining your skills and stay consistent with your preparation."
        if is_placed else
        "Your current profile is below the threshold typically associated with "
        "placement success. Focus on the areas below to improve your standing."
    )

    st.markdown(f"""
    <div class="result-card {status_class}">
        <div class="status-eyebrow">// Predicted Outcome</div>
        <div class="status-title {status_class}">{status_title}</div>
        <div class="status-desc">{status_desc}</div>
        <div class="stat-tags">
            <div class="stat-tag">Status: <b>{status_label}</b></div>
            <div class="stat-tag">Confidence: <b>{confidence_pct}%</b></div>
            <div class="stat-tag">Placement Chance: <b>{placement_chance_pct}%</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    '<div class="footer-note">[ MODEL: RandomForestClassifier ] · '
    'prediction is an estimate, not a guarantee</div>',
    unsafe_allow_html=True
)