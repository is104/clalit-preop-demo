import streamlit as st

st.set_page_config(
    page_title="Clalit - טרום ניתוח",
    layout="centered"
)

# -------------------------
# MOBILE CSS
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

.stButton button {
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
    "intro": "שלום 👋 אני העוזר הדיגיטלי לפני ניתוח. נתחיל באיסוף מידע רפואי.",
    "allergies": "האם יש לך אלרגיות לתרופות?",
    "medications": "אילו תרופות אתה נוטל ביום-יום?",
    "anesthesia": "האם היו בעיות בהרדמות קודמות?",
    "mobility": "מה רמת התפקוד שלך ביום-יום?",
    "summary": "תודה 🙏 סיימנו את התהליך"
}

# -------------------------
# STATE INIT
# -------------------------

if "i" not in st.session_state:
    st.session_state.i = 0

if "chat" not in st.session_state:
    st.session_state.chat = []

if "data" not in st.session_state:
    st.session_state.data = {}

if "started" not in st.session_state:
    st.session_state.started = False

state = STEPS[st.session_state.i]

# -------------------------
# INTRO SCREEN (FIXED)
# -------------------------

if not st.session_state.started:

    st.title("🏥 טרום ניתוח - Clalit")

    st.markdown("""
    מערכת דיגיטלית לאיסוף מידע רפואי לפני ניתוח  
    התהליך לוקח כ-2 דקות בלבד.
    """)

    if st.button("▶ התחל תהליך", use_container_width=True):

        st.session_state.started = True

        st.session_state.chat.append({
            "role": "bot",
            "text": QUESTIONS["intro"]
        })

        st.rerun()

    st.stop()

# -------------------------
# CHAT RENDER
# -------------------------

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

# -------------------------
# INPUT
# -------------------------

st.markdown("---")

user_input = st.text_input("הקלד תשובה כאן")

if st.button("שלח", use_container_width=True):

    if not user_input:
        st.stop()

    # user message
    st.session_state.chat.append({
        "role": "user",
        "text": user_input
    })

    current_state = STEPS[st.session_state.i]

    # save structured data (skip intro + summary)
    if current_state not in ["intro", "summary"]:
        st.session_state.data[current_state] = user_input

    # move forward
    st.session_state.i += 1

    # next question
    if st.session_state.i < len(STEPS):

        next_state = STEPS[st.session_state.i]

        st.session_state.chat.append({
            "role": "bot",
            "text": QUESTIONS[next_state]
        })

    st.rerun()

# -------------------------
# SUMMARY
# -------------------------

st.markdown("---")

st.subheader("📋 סיכום רפואי")

st.json(st.session_state.data)
