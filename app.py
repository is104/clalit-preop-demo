import streamlit as st

st.set_page_config(
    page_title="Clalit - טרום ניתוח",
    layout="centered"
)

# -------------------------
# CSS (mobile)
# -------------------------

st.markdown("""
<style>
.block-container {
    max-width: 420px;
    padding-top: 1rem;
}

.chat {
    padding: 14px;
    border-radius: 14px;
    margin: 8px 0;
}

.bot {
    background: #f1f3f5;
}

.user {
    background: #dbeafe;
    text-align: right;
}

button {
    width: 100% !important;
    height: 50px !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# FLOW
# -------------------------

STEPS = [
    "intro",
    "allergies",
    "medications",
    "anesthesia",
    "mobility",
    "summary"
]

QUESTIONS = {
    "intro": "שלום 👋 נתחיל באיסוף מידע לפני ניתוח.",
    "allergies": "האם יש לך אלרגיות לתרופות?",
    "medications": "אילו תרופות אתה נוטל ביום-יום?",
    "anesthesia": "האם היו בעיות בהרדמות קודמות?",
    "mobility": "מה רמת התפקוד שלך?",
    "summary": "תודה 🙏 סיימנו"
}

# -------------------------
# STATE
# -------------------------

if "i" not in st.session_state:
    st.session_state.i = 0

if "started" not in st.session_state:
    st.session_state.started = False

if "data" not in st.session_state:
    st.session_state.data = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

state = STEPS[st.session_state.i]

# -------------------------
# INTRO (FIXED - NO CHAT INJECTION)
# -------------------------

if not st.session_state.started:

    st.title("🏥 טרום ניתוח - Clalit")

    st.markdown("""
מערכת דיגיטלית לאיסוף מידע רפואי לפני ניתוח.
התהליך קצר ופשוט.
""")

    if st.button("▶ התחל"):

        st.session_state.started = True

        # רק הודעת פתיחה אחת!
        st.session_state.messages.append({
            "role": "bot",
            "text": QUESTIONS["intro"]
        })

        st.rerun()

    st.stop()

# -------------------------
# BOT MESSAGE (single source of truth)
# -------------------------

def current_question():
    return QUESTIONS[STEPS[st.session_state.i]]

# -------------------------
# RENDER CHAT
# -------------------------

for m in st.session_state.messages:

    if m["role"] == "bot":
        st.markdown(f"<div class='chat bot'>🧑‍⚕️ {m['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat user'>👤 {m['text']}</div>", unsafe_allow_html=True)

# -------------------------
# INPUT
# -------------------------

st.markdown("---")

user_input = st.text_input("כתוב תשובה")

if st.button("שלח"):

    if user_input.strip() == "":
        st.stop()

    # save user message
    st.session_state.messages.append({
        "role": "user",
        "text": user_input
    })

    # save structured data (skip intro + summary)
    if state not in ["intro", "summary"]:
        st.session_state.data[state] = user_input

    # move forward
    st.session_state.i += 1

    # add next bot message ONLY if exists
    if st.session_state.i < len(STEPS):

        next_q = QUESTIONS[STEPS[st.session_state.i]]

        st.session_state.messages.append({
            "role": "bot",
            "text": next_q
        })

    st.rerun()

# -------------------------
# SUMMARY
# -------------------------

st.markdown("---")
st.subheader("📋 סיכום רפואי")
st.json(st.session_state.data)
