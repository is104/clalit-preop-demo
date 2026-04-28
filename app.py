import streamlit as st

st.set_page_config(page_title="Clalit Pre-Op Demo", layout="centered")

# -------------------------
# STATE
# -------------------------

STATES = [
    "intro",
    "allergies",
    "medications",
    "anesthesia",
    "summary"
]

QUESTIONS = {
    "intro": "שלום 👋 נתחיל באיסוף מידע לפני ניתוח. האם אתה מוכן?",
    "allergies": "האם יש לך אלרגיות לתרופות?",
    "medications": "אילו תרופות אתה נוטל?",
    "anesthesia": "האם היו בעיות בהרדמות קודמות?",
    "summary": "תודה, סיימנו את האיסוף."
}

PATIENTS = {
    "normal": {
        "allergies": "none",
        "medications": "none",
        "anesthesia": "none"
    },
    "high_risk": {
        "allergies": "penicillin - anaphylaxis",
        "medications": "warfarin",
        "anesthesia": "complication in past surgery"
    }
}

def check_risk(data):
    flags = []
    if "anaphylaxis" in data.get("allergies", ""):
        flags.append("SEVERE_ALLERGY")
    if "warfarin" in data.get("medications", ""):
        flags.append("ANTICOAGULANT")
    if "complication" in data.get("anesthesia", ""):
        flags.append("ANESTHESIA_RISK")
    return flags

# -------------------------
# UI STATE
# -------------------------

if "i" not in st.session_state:
    st.session_state.i = 0

if "data" not in st.session_state:
    st.session_state.data = {}

st.title("🏥 Clalit Pre-Op Intake Demo")

mode = st.sidebar.selectbox("Patient Type", ["normal", "high_risk"])

if st.sidebar.button("Reset"):
    st.session_state.i = 0
    st.session_state.data = {}

state = STATES[st.session_state.i]

st.subheader(f"Step: {state}")
st.info(QUESTIONS[state])

# -------------------------
# SIMULATION
# -------------------------

if st.button("Next Step"):

    if state == "summary":
        st.success("Demo completed")
        st.stop()

    if state != "intro":
        answer = PATIENTS[mode][state]
        st.write("👤 Patient:", answer)
        st.session_state.data[state] = answer

        risks = check_risk(st.session_state.data)

        if risks:
            st.error(f"🚨 ESCALATION: {risks}")
            st.stop()

    st.session_state.i += 1
    st.rerun()

st.divider()

st.subheader("📊 Collected Data")
st.json(st.session_state.data)
