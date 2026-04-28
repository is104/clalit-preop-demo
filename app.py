import streamlit as st

st.set_page_config(
    page_title="Clalit - טרום ניתוח",
    layout="centered"
)

# -------------------------
# MOBILE STYLING
# -------------------------

st.markdown("""
<style>
.block-container {
    max-width: 420px;
    padding-top: 1rem;
}

.chat-bubble {
    padding: 14px;
    border-radius: 16px;
    margin: 10px 0;
    font-size: 16px;
    line-height: 1.5;
}

.bot {
    background-color: #f1f3f5;
}

.user {
    background-color: #dbeafe;
    text-align: right;
}

.big-button button {
    width: 100%;
    height: 52px;
    border-radius: 12px;
    font-size: 16px;
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
    "intro": "שלום 👋 אני עוזר דיגיטלי לפני ניתוח. נתחיל?",
    "allergies": "האם יש לך אלרגיות לתרופות?",
    "medications": "אילו תרופות אתה נוטל ביום-יום?",
    "anesthesia": "האם היו בעיות בהרדמות קודמות?",
    "mobility": "מה רמת התפקוד שלך ביום-יום?",
    "summary": "תודה 🙏 סיימנו את הבדיקה"
}

# -------------------------
# SIMULATED PATIENT (for demo)
# -------------------------

PATIENT = {
    "allergies": "אין",
    "medications": "warfarin",
    "anesthesia": "סיבוך בניתוח קודם",
    "mobility": "עצמאי"
}

# -------------------------
# STATE
# -------------------------

if "i" not in st.session_state:
    st.session_state.i = 0

if "chat" not in st.session_state:
    st.session_state.chat = []

if "data" not in st.session_state:
    st.session_state.data = {}

state = STEPS[st.session_state.i]

# -------------------------
# CHAT DISPLAY
# -------------------------

def render_chat():

    for msg in st.session_state.chat:

        if msg["role"] == "bot":
            st.markdown(
                f"<div class='chat-bubble bot'>🧑‍⚕️ {msg['text']}</div>",
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                f"<div class='chat-bubble user'>👤 {msg['text']}</div>",
                unsafe_allow_html=True
            )

render_chat()

# -------------------------
# BOT QUESTION
# -------------------------

if len(st.session_state.chat) == 0:
    st.session_state.chat.append({
        "role": "bot",
        "text": QUESTIONS[state]
    })

# -------------------------
# INPUT (mobile style)
# -------------------------

st.markdown("---")

user_input = st.text_input("כתוב תשובה כאן")

if st.button("שלח", use_container_width=True):

    # store user message
    st.session_state.chat.append({
        "role": "user",
        "text": user_input
    })

    # save structured data
    if state != "intro" and state != "summary":
        st.session_state.data[state] = user_input

    # simulate safety check
    if "warfarin" in user_input or "סיבוך" in user_input:
        st.error("🚨 נדרש בירור אחות / רופא")

    # move forward
    st.session_state.i += 1

    if st.session_state.i < len(STEPS):

        next_state = STEPS[st.session_state.i]

        st.session_state.chat.append({
            "role": "bot",
            "text": QUESTIONS[next_state]
        })

    st.rerun()

# -------------------------
# SUMMARY (mobile friendly)
# -------------------------

st.markdown("---")

st.markdown("### 📋 סיכום רפואי")

st.json(st.session_state.data)
