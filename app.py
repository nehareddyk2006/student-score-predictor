import streamlit as st
import joblib

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Student Predictor", layout="centered")

# ---------------- STYLE FUNCTION ----------------
def apply_styles():
    st.markdown("""
    <style>

    /* Background */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa, #e4e8f0) !important;
    }

    /* Titles */
    h1, h2, h3 {
        color: #2c3e50 !important;
        text-align: center;
    }

    /* Labels */
    label {
        color: #34495e !important;
    }

    /* Inputs */
    .stNumberInput, .stSlider {
        background: white !important;
        border-radius: 10px;
        padding: 8px;
        border: 1px solid #ddd;
    }

    /* Button */
    .stButton>button {
        background: linear-gradient(to right, #4facfe, #00c6ff) !important;
        color: white !important;
        border-radius: 10px;
        font-weight: bold;
        height: 3em;
        width: 100%;
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0px 8px 18px rgba(0,0,0,0.1);
    }

    /* ALERT BOX FIX */
    div[data-testid="stAlert"] {
        color: #2c3e50 !important;
        font-weight: 500;
    }

    div[data-testid="stAlert"][kind="success"] {
        background-color: #d4edda !important;
        color: #155724 !important;
    }

    div[data-testid="stAlert"][kind="warning"] {
        background-color: #fff3cd !important;
        color: #856404 !important;
    }

    div[data-testid="stAlert"][kind="error"] {
        background-color: #f8d7da !important;
        color: #721c24 !important;
    }

    /* CHECKBOX FIX */
    div[data-testid="stCheckbox"] label {
        color: #2c3e50 !important;
        font-weight: 500;
    }

    div[data-testid="stCheckbox"] > div {
        background-color: white !important;
        border-radius: 6px;
    }

    div[data-testid="stCheckbox"] {
        margin-bottom: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = joblib.load("model.pkl")

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "input"

# ---------------- PAGE 1 ----------------
if st.session_state.page == "input":
    apply_styles()

    st.title("📊 Student Performance Predictor")
    st.markdown("### Smart AI-based score prediction system")

    st.subheader("📋 Enter Your Details")

    hours = st.number_input("📚 Study Hours", min_value=0.0)
    attendance = st.number_input("🏫 Attendance (%)", min_value=0.0)
    sleep = st.number_input("😴 Sleep Hours", min_value=0.0)
    prev_score = st.number_input("📊 Previous Score", min_value=0.0)
    stress = st.slider("😵 Stress Level", 1, 10)
    focus = st.slider("🎯 Focus Level", 1, 10)
    activity = st.slider("🏃 Physical Activity (days/week)", 0, 7)

    if st.button("Predict Score 🚀"):
        st.session_state.data = {
            "hours": hours,
            "attendance": attendance,
            "sleep": sleep,
            "prev_score": prev_score,
            "stress": stress,
            "focus": focus,
            "activity": activity
        }
        st.session_state.page = "result"
        st.rerun()

# ---------------- PAGE 2 ----------------
elif st.session_state.page == "result":
    apply_styles()

    st.title("🎯 Your Predicted Score")

    data = st.session_state.data

    base = model.predict([[data["hours"]]])[0]

    final_score = (
        base +
        (data["attendance"] * 0.1) +
        (data["sleep"] * 1.5) +
        (data["focus"] * 2) -
        (data["stress"] * 1.5) +
        (data["activity"] * 1)
    )

    final_score = min(final_score, 100)

    st.markdown(f"### 📊 Score: {round(final_score,2)}")

    if final_score < 50:
        st.error("😬 Needs improvement")
    elif final_score < 75:
        st.warning("🙂 You're getting there")
    else:
        st.success("🔥 Excellent!")

    if st.button("View Improvement Tips 📈"):
        st.session_state.score = final_score
        st.session_state.page = "improve"
        st.rerun()

# ---------------- PAGE 3 ----------------
elif st.session_state.page == "improve":
    apply_styles()

    score = st.session_state.score

    st.title("📈 Improve Your Score")
    st.write(f"Your current predicted score: **{round(score,2)}**")

    st.subheader("💡 Suggestions")

    if score < 50:
        st.warning("Increase study hours, reduce stress, and improve sleep.")
    elif score < 75:
        st.info("Work on consistency, focus, and attendance.")
    else:
        st.success("You're doing amazing! Maintain your routine.")

    st.markdown("### 🔧 Action Tracker")

    st.checkbox("📚 Study 2+ more hours daily")
    st.checkbox("😴 Maintain 7–8 hours sleep")
    st.checkbox("🧘 Reduce stress (meditation/exercise)")
    st.checkbox("📵 Avoid distractions for better focus")

    if st.button("🔙 Back to Home"):
        st.session_state.page = "input"
        st.rerun()
