import streamlit as st
import uuid
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Clalit - מערכת טרום ניתוח",
    layout="wide"
)

# =========================
# STATE STORAGE (demo only)
# =========================

if "patients" not in st.session_state:
    st.session_state.patients = {}

if "active_patient" not in st.session_state:
    st.session_state.active_patient = None

# =========================
# CREATE PATIENT
# =========================

def create_patient(name, risk_level):

    pid = str(uuid.uuid4())[:8]

    st.session_state.patients[pid] = {
        "id": pid,
        "name": name,
        "risk": risk_level,
        "created_at": str(datetime.now()),
        "data": {},
        "flags": [],
        "status": "בתהליך"
    }

    return pid

# =========================
# SAFETY ENGINE
# =========================

def check_flags(data):

    flags = []

    if "אנפילקסיס" in str(data.get("אלרגיות", "")):
        flags.append("סיכון אלרגי חמור")

    if any(x in str(data.get("תרופות", "")) for x in ["warfarin", "eliquis"]):
        flags.append("נוגדי קרישה")

    if "סיבוך" in str(data.get("הרדמה", "")):
        flags.append("היסטוריה הרדמתית מורכבת")

    return flags

# =========================
# SIDEBAR - NURSE DASHBOARD
# =========================

st.sidebar.title("🏥 לוח בקרה")

st.sidebar.subheader("➕ יצירת מטופל חדש")

name = st.sidebar.text_input("שם מטופל")
risk = st.sidebar.selectbox("רמת סיכון", ["רגיל", "גבוה"])

if st.sidebar.button("צור מטופל"):
    if name:
        pid = create_patient(name, risk)
        st.sidebar.success(f"נוצר מטופל: {pid}")

st.sidebar.divider()

st.sidebar.subheader("👥 מטופלים פעילים")

for pid, p in st.session_state.patients.items():
    if st.sidebar.button(f"{p['name']} ({pid})"):
        st.session_state.active_patient = pid

# =========================
# MAIN VIEW
# =========================

st.title("🏥 מערכת טרום ניתוח - Clalit")

if not st.session_state.active_patient:
    st.info("בחר מטופל מהצד שמאל כדי להתחיל")
    st.stop()

patient = st.session_state.patients[st.session_state.active_patient]

st.subheader(f"מטופל: {patient['name']} ({patient['id']})")

col1, col2 = st.columns(2)

# =========================
# LEFT: CLINICAL FORM
# =========================

with col1:

    st.markdown("### 📋 טופס רפואי")

    allergies = st.multiselect(
        "אלרגיות",
        ["אין", "פניצילין", "לטקס", "אנפילקסיס"]
    )

    meds = st.text_area("תרופות קבועות")

    anesthesia = st.radio(
        "בעיות בהרדמה קודמת?",
        ["לא", "כן"]
    )

    mobility = st.selectbox(
        "תפקוד יומי",
        ["עצמאי", "עזרה חלקית", "מוגבל"]
    )

    if st.button("שמור נתונים"):

        patient["data"] = {
            "אלרגיות": allergies,
            "תרופות": meds,
            "הרדמה": anesthesia,
            "תפקוד": mobility
        }

        patient["flags"] = check_flags(patient["data"])

        if patient["flags"]:
            patient["status"] = "⚠️ נדרש בדיקת אחות"
        else:
            patient["status"] = "תקין"

        st.success("נשמר בהצלחה")

# =========================
# RIGHT: CLINICAL VIEW
# =========================

with col2:

    st.markdown("### 🧑‍⚕️ תצוגה קלינית")

    st.write("סטטוס:")
    st.success(patient["status"])

    st.write("נתונים:")
    st.json(patient["data"])

    if patient["flags"]:
        st.error("🚨 התראות קליניות")
        st.write(patient["flags"])

# =========================
# EDUCATION MODULE (HEBREW)
# =========================

st.divider()

st.markdown("## 🧑‍⚕️ מידע למטופל (הכנה לניתוח)")

st.markdown("""
### מה צפוי לפני הניתוח?
- בדיקות דם
- פגישה עם רופא מרדים
- צום של 6–8 שעות לפני הניתוח

### סיכונים כלליים
- דימום (נדיר)
- זיהום (נדיר)
- תגובה להרדמה

### הוראות חשובות
- יש לדווח על כל תרופה קבועה
- אין לאכול לפני הניתוח
- יש להגיע בזמן לבית החולים
""")

# =========================
# AUDIT LOG
# =========================

st.divider()

st.markdown("## 🧾 יומן קליני (Audit)")

st.json({
    "מטופל": patient["name"],
    "סטטוס": patient["status"],
    "דגלים": patient["flags"],
    "נתונים": patient["data"]
})
