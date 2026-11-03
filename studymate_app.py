# ============================================================
# AI STUDYMATE - Student Performance Predictor (UI)
# Run:  python train.py      (pehle ek baar)
#       streamlit run studymate_app.py
# pip install streamlit plotly pandas scikit-learn joblib
# ============================================================

import os
import joblib
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="AI StudyMate", page_icon="🎓", layout="wide")

SUBJECTS = ["math_score", "reading_score", "writing_score"]
LABELS = {"math_score": "Math", "reading_score": "Reading", "writing_score": "Writing"}

# ============================================================
# 1. STYLE
# ============================================================

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#0b0b2b 0%,#16124a 60%,#1d1566 100%); color:#fff;}
[data-testid="stSidebar"] {background:#0a0a26; border-right:1px solid #2a2670;}
[data-testid="stHeader"] {background:transparent;}
div[data-testid="stVerticalBlockBorderWrapper"] {
  background:rgba(255,255,255,0.05); border:1px solid #4b3fd1 !important;
  border-radius:18px; padding:6px;}
.stButton>button {background:linear-gradient(90deg,#7c3aed,#4f46e5); color:#fff; border:none;
  border-radius:12px; padding:10px; font-weight:700;}
.stButton>button:hover {filter:brightness(1.15); color:#fff;}
label, .stMarkdown p {color:#e8e8ff !important;}
.title {font-size:34px; font-weight:800;}
.title span {color:#8b5cf6;}
.sub {color:#b9b9e8; margin-bottom:14px;}
.hero {background:linear-gradient(120deg,#0c3b3a,#14124a); border:1px solid #1fbf8a;
  border-radius:18px; padding:22px;}
.pill {display:inline-block; background:rgba(34,229,139,0.15); color:#22e58b;
  border-radius:20px; padding:4px 14px; font-weight:700;}
.big {font-size:56px; font-weight:800; line-height:1.1;}
.green {color:#22e58b; font-weight:700;}
.card-title {font-size:18px; font-weight:700; margin-bottom:8px;}
.tag {display:inline-block; border-radius:8px; padding:3px 10px; font-weight:700; font-size:13px;}
.good {background:rgba(34,229,139,0.15); color:#22e58b; border:1px solid #22e58b;}
.avg {background:rgba(245,165,36,0.15); color:#f5a524; border:1px solid #f5a524;}
.bad {background:rgba(244,63,94,0.15); color:#f43f5e; border:1px solid #f43f5e;}
.muted {color:#b9b9e8; font-size:13px;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. LOAD TRAINED MODELS
# ============================================================


@st.cache_resource
def load_all():
    models = {s: joblib.load(f"model_{s}.pkl") for s in SUBJECTS}
    feature_map = joblib.load("feature_map.pkl")
    reference = pd.read_csv("reference_marks.csv")
    return models, feature_map, reference


if not os.path.exists("feature_map.pkl"):
    st.error("Pehle `python train.py` chalao, phir ye app kholo.")
    st.stop()

models, feature_map, reference = load_all()

# ============================================================
# 3. HELPER FUNCTIONS
# ============================================================


def status(mark):
    if mark >= 80:
        return "Good", "good", "#22e58b"
    if mark >= 65:
        return "Average", "avg", "#f5a524"
    return "Needs Improvement", "bad", "#f43f5e"


def overall_label(score):
    if score >= 85:
        return "Excellent", "#22e58b"
    if score >= 70:
        return "Good", "#22e58b"
    if score >= 55:
        return "Average", "#f5a524"
    return "Needs Improvement", "#f43f5e"


def donut(value, color):
    fig = go.Figure(go.Pie(
        values=[value, 100 - value], hole=0.75, sort=False, textinfo="none", hoverinfo="skip",
        marker=dict(colors=[color, "rgba(255,255,255,0.08)"])))
    fig.update_layout(
        showlegend=False, height=150, margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(text=f"{value:.0f}%", x=0.5, y=0.5, showarrow=False,
                          font=dict(size=22, color="white"))])
    return fig


def analyze(marks, test_prep):
    """Return per-subject expected marks, gap, percentile."""
    info = {}
    values = dict(marks)
    values["test_prep"] = test_prep
    for s in SUBJECTS:
        row = pd.DataFrame([[values[f] for f in feature_map[s]]], columns=feature_map[s])
        expected = float(models[s].predict(row)[0])
        percentile = float((reference[s] < marks[s]).mean() * 100)
        info[s] = {"expected": expected, "gap": marks[s] - expected, "percentile": percentile}
    return info


def make_plan(marks):
    order = sorted(SUBJECTS, key=lambda s: marks[s])
    a, b = LABELS[order[0]], LABELS[order[1]]
    return [
        f"Day 1: {a} ke basic concepts revise karo",
        f"Day 2: {a} ke 20 practice questions solve karo",
        f"Day 3: {b} ka weak part revise karo",
        f"Day 4: {a} ka mini test do",
        f"Day 5: {b} ke practice questions solve karo",
        "Day 6: Sab subjects ke previous year questions solve karo",
        "Day 7: Full mock test do aur galtiyan note karo",
    ]


# ============================================================
# 4. SIDEBAR + HEADER
# ============================================================

with st.sidebar:
    st.markdown("<div style='text-align:center;font-size:44px'>🎓</div>"
                "<div style='text-align:center;font-size:22px;font-weight:800'>AI StudyMate</div>"
                "<div style='text-align:center;color:#b9b9e8;font-size:12px'>Predict • Analyze • Improve</div>",
                unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**🏠 Dashboard**")
    st.markdown("📅 Study Planner")
    st.markdown("📊 Analytics")
    st.markdown("ℹ️ About")
    st.markdown("---")
    st.markdown("🚀 **Dream Big, Study Smart!**")

st.markdown("<div class='title'>AI Student Performance <span>Predictor</span></div>"
            "<div class='sub'>Enter your details, analyze your performance and get personalized study suggestions.</div>",
            unsafe_allow_html=True)

left, right = st.columns([1, 2.2], gap="medium")

# ============================================================
# 5. LEFT PANEL
# ============================================================

with left:
    with st.container(border=True):
        st.markdown("<div class='card-title'>👤 Student Details & Marks</div>", unsafe_allow_html=True)
        sid = st.text_input("Student ID", "STU2026001")
        name = st.text_input("Name", "Md Danish Ali")
        course = st.selectbox("Course", ["BCA", "BTech CSE", "MCA", "BSc IT"])
        st.caption("Subjects dataset ke hisab se hain (Math, Reading, Writing).")

        marks = {}
        cols = st.columns(3)
        defaults = {"math_score": 70, "reading_score": 72, "writing_score": 68}
        for col, s in zip(cols, SUBJECTS):
            marks[s] = col.number_input(LABELS[s], 0, 100, defaults[s])

        prep = st.selectbox("Test Preparation Course", ["none", "completed"])
        test_prep = 1 if prep == "completed" else 0

        if st.button("✨ Analyze Performance  →", use_container_width=True):
            st.session_state["ran"] = True

if not st.session_state.get("ran"):
    with right:
        st.info("Left side mein marks bharo aur **Analyze Performance** dabao.")
    st.stop()

# ============================================================
# 6. ANALYSIS
# ============================================================

info = analyze(marks, test_prep)
overall = sum(marks.values()) / len(marks)
ref_overall = reference[SUBJECTS].mean(axis=1)
overall_pct = float((ref_overall < overall).mean() * 100)
label, label_color = overall_label(overall)

best = max(SUBJECTS, key=lambda s: marks[s])
worst = min(SUBJECTS, key=lambda s: marks[s])
need = max(0, 80 - marks[worst])
below_expected = [LABELS[s] for s in SUBJECTS if info[s]["gap"] < -5]
needs_work = [LABELS[s] for s in SUBJECTS if marks[s] < 80]

# ============================================================
# 7. RIGHT PANEL
# ============================================================

with right:
    st.markdown(
        "<div class='hero'><span class='pill'>✅ Prediction Result</span>"
        f"<div style='margin-top:10px;font-size:20px;font-weight:700'>{name}, your overall performance is</div>"
        f"<div class='big' style='color:{label_color}'>{label}</div>"
        f"<div style='margin-top:8px'>Estimated Score: <span class='green'>{overall:.1f}%</span>"
        f" &nbsp;|&nbsp; Better than <span class='green'>{overall_pct:.0f}%</span> students in dataset</div>"
        "</div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<div class='card-title'>📈 Subject-wise Analysis</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        for col, s in zip(cols, SUBJECTS):
            lab, css, color = status(marks[s])
            with col:
                st.markdown(f"<div style='text-align:center;font-weight:700'>{LABELS[s]}</div>",
                            unsafe_allow_html=True)
                st.plotly_chart(donut(marks[s], color), use_container_width=True,
                                config={"displayModeBar": False}, key=f"d_{s}")
                st.markdown(
                    f"<div style='text-align:center'><span class='tag {css}'>{lab}</span>"
                    f"<div class='muted'>Expected: {info[s]['expected']:.0f} | "
                    f"Top {100 - info[s]['percentile']:.0f}%</div></div>", unsafe_allow_html=True)

# ============================================================
# 8. BOTTOM CARDS
# ============================================================

b1, b2, b3 = st.columns([1.2, 1, 1], gap="medium")

with b1:
    with st.container(border=True):
        st.markdown("<div class='card-title'>🎯 Personalized Study Plan <span class='tag good'>7 Days</span></div>",
                    unsafe_allow_html=True)
        st.markdown(f"Focus more on: <span class='green'>{LABELS[worst]}</span> (Need +{need:.0f} marks for 80)",
                    unsafe_allow_html=True)
        plan = make_plan(marks)
        for item in plan[:3]:
            st.markdown(f"✅ {item}")
        with st.expander("View Full Study Plan →"):
            for item in plan:
                st.markdown(f"✅ {item}")

with b2:
    with st.container(border=True):
        st.markdown("<div class='card-title'>💡 Key Insights</div>", unsafe_allow_html=True)
        below = ", ".join(below_expected) if below_expected else "None"
        improve = ", ".join(needs_work) if needs_work else "None"
        st.markdown(
            f"🏆 Best Subject: **{LABELS[best]} ({marks[best]})**<br><br>"
            f"⚠️ Weakest Subject: **{LABELS[worst]} ({marks[worst]})**<br><br>"
            f"📉 Below expected: **{below}**<br><br>"
            f"🛠️ Need improvement: **{improve}**<br><br>"
            f"⭐ Overall: **{label}**", unsafe_allow_html=True)

with b3:
    with st.container(border=True):
        st.markdown("<div class='card-title'>🛠️ Next Steps</div>", unsafe_allow_html=True)
        tip = "Test preparation course complete karo" if test_prep == 0 else "Test prep jaari rakho"
        st.markdown(
            f"**1.** Focus on **{LABELS[worst]}**<br><br>"
            "**2.** Take mock tests regularly<br><br>"
            f"**3.** {tip}<br><br>"
            "**4.** Track your progress weekly", unsafe_allow_html=True)