import streamlit as st
import json
import os

# -------------------------
# PAGE CONFIG (MOBILE FEEL)
# -------------------------

st.set_page_config(
    page_title="Clalit Pre-Op AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------
# CUSTOM MOBILE CSS
# -------------------------

st.markdown("""
<style>
/* Mobile-first styling */
.block-container {
    padding-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 500px;
}

/* Question card */
.card {
    padding: 18px;
    border-radius: 16px;
    background-color: #f6f8fa;
    margin-bottom: 12px;
    font-size: 18px;
}

/* Buttons */
.stButton button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    font-size: 16px;
}

/* Progress */
.progress {
    font-size: 14px;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# WORKFLOW
# -------------------------

STATES = [
    "intro",
    "allergies",
    "medications",
    "anesthesia",
    "chronic_conditions",
    "summary"
]

QUESTIONS = {
    "intro": "שלום 👋 האם נתחיל באיסוף מידע לפני ניתוח?",
    "allergies": "האם יש לך אלרגיות לתרופות?",
    "medications": "אילו תרופות אתה נוטל?",
    "anesthesia": "האם היו בעיות בהרדמות קודמות?",
    "chronic_conditions": "האם יש לך מחלות כרוניות?",
    "summary": "תודה — סיימנו 🙏"
}

PATIENTS = {
    "normal": {
        "allergies": "none",
        "medications": "none",
        "anesthesia": "none",
        "chronic_conditions": "none"
    },
    "high_risk": {
        "allergies": "penicillin - anaphylaxis",
        "medications": "warfarin",
        "anesthesia": "complication in previous surgery",
        "chronic_conditions": "cardiac disease"
    }
}

# -------------------------
# STATE INIT
# -------------------------

if "i" not in st.session_state:
    st.session_state.i = 0

if "data" not in st.session_state:
    st.session_state.data = {}

# -------------------------
# HEADER (MOBILE STYLE)
# -------------------------

st.title("🏥 Pre-Op Intake")

mode = st.selectbox("Patient Type", ["normal", "high_risk"])

state = STATES[st.session_state.i]
question = QUESTIONS[state]

# -------------------------
# PROGRESS BAR
# -------------------------

progress = int((st.session_state.i / (len(STATES)-1)) * 100)

st.markdown(f"<div class='progress'>Progress: {progress}%</div>", unsafe_allow_html=True)
st.progress(progress)

# -------------------------
# QUESTION CARD
# -------------------------

st.markdown(f"""
<div class="card">
<b>{question}</b>
</div>
""", unsafe_allow_html=True)

# -------------------------
# SIMULATED PATIENT ANSWER
# -------------------------

def get_answer(state):
    return PATIENTS[mode].get(state, "")

# -------------------------
# ACTION BUTTONS (MOBILE STYLE)
# -------------------------

col1, col2 = st.columns(2)

with col1:
    next_btn = st.button("➡️ Next")

with col2:
    reset_btn = st.button("🔄 Reset")

if reset_btn:
    st.session_state.i = 0
    st.session_state.data = {}
    st.rerun()

# -------------------------
# FLOW LOGIC
# -------------------------

if next_btn:

    if state == "summary":
        st.success("Completed")
        st.stop()

    if state != "intro":

        answer = get_answer(state)

        st.markdown(f"""
        <div class="card">
        👤 <b>Patient:</b> {answer}
        </div>
        """, unsafe_allow_html=True)

        st.session_state.data[state] = answer

        # simple escalation
        if "anaphylaxis" in answer or "warfarin" in answer:
            st.error("🚨 CLINICAL ALERT: Requires nurse review")
            st.stop()

    st.session_state.i += 1
    st.rerun()

# -------------------------
# SUMMARY (CLEAN MOBILE VIEW)
# -------------------------

st.divider()

st.subheader("📊 Summary")

st.json(st.session_state.data)
