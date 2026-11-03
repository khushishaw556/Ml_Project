# ============================================================
# STEP 3: studymate_v2.py  (AI StudyMate dashboard)
# Run:  python -m streamlit run studymate_v2.py
# (pehle make_dataset.py aur train_courses.py chala lo)
# ============================================================

import os
import joblib
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="StudyMate | Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
)

# ============================================================
# 1. STYLE
# ============================================================

st.markdown("""
<style>
:root {
  --navy: #172033;
  --text: #374151;
  --muted: #6b7280;
  --line: #e6eaf0;
  --blue: #3454d1;
  --blue-soft: #edf1ff;
  --teal: #0f9f8f;
}
.stApp {background:#f5f7fb; color:var(--navy);}
[data-testid="stSidebar"] {background:#ffffff; border-right:1px solid var(--line);}
[data-testid="stHeader"] {background:transparent;}
[data-testid="stVerticalBlockBorderWrapper"] {
  background:#ffffff; border:1px solid var(--line) !important;
  border-radius:14px; padding:16px; box-shadow:0 8px 24px rgba(23,32,51,0.04);}
.stButton>button {
  background:var(--blue); color:#fff; border:none; border-radius:10px;
  height:46px; font-weight:700;}
.stButton>button:hover {background:#2944b8; color:#fff; border:none;}
label {color:var(--text) !important; font-weight:600;}
.stMarkdown p {color:var(--text);}
.page-header {
  background:linear-gradient(120deg,#172033 0%,#27365c 100%);
  border-radius:16px; padding:24px 28px; margin-bottom:18px; color:#fff;
  box-shadow:0 12px 30px rgba(23,32,51,0.12);}
.page-header h1 {font-size:30px; line-height:1.15; margin:0 0 8px 0; color:#fff;}
.page-header p {font-size:15px; margin:0; color:#cbd5e1;}
.brand {text-align:center; padding:8px 0 4px;}
.brand-icon {font-size:38px;}
.brand-name {font-size:21px; font-weight:800; color:var(--navy); margin-top:4px;}
.brand-tagline {font-size:12px; color:var(--muted);}
.hero {
  background:linear-gradient(120deg,#eefbf8,#eef2ff);
  border:1px solid #d9e8e4; border-radius:14px; padding:22px;
  display:flex; justify-content:space-between; align-items:center;}
.pill {display:inline-block; background:#dff7f1; color:#087c70;
  border-radius:20px; padding:5px 12px; font-size:12px; font-weight:800;}
.big {font-size:42px; font-weight:800; line-height:1.1; color:#172033;}
.green {color:var(--teal); font-weight:800;}
.card-title {font-size:17px; font-weight:800; color:var(--navy); margin-bottom:8px;}
.tag {display:inline-block; border-radius:20px; padding:4px 10px; font-weight:800; font-size:12px;}
.good {background:#e7f7f2; color:#087c70; border:1px solid #bfe6dc;}
.avg {background:#fff6df; color:#9a6700; border:1px solid #f1d59a;}
.bad {background:#fff0f0; color:#b42318; border:1px solid #f2c4c0;}
.muted {color:var(--muted); font-size:12px;}
.subname {text-align:center; font-weight:800; font-size:13px; min-height:36px; color:var(--navy);}
.empty-state {
  min-height:300px; border:1px dashed #ccd5e4; border-radius:14px;
  background:#fff; display:flex; flex-direction:column; align-items:center;
  justify-content:center; text-align:center; padding:32px; color:var(--muted);}
.empty-state-icon {font-size:44px; margin-bottom:10px;}
.empty-state strong {color:var(--navy); font-size:18px;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. LOAD MODELS / DATA
# ============================================================

if not os.path.exists("meta.pkl"):
    st.error("Pehle `python make_dataset.py` aur `python train_courses.py` chalao.")
    st.stop()


def slug(course):
    return course.replace(" ", "_")


@st.cache_resource
def load_meta():
    return joblib.load("meta.pkl")


@st.cache_resource
def load_models(course):
    meta = load_meta()
    return {s: joblib.load(p) for s, p in meta[course]["files"].items()}


@st.cache_data
def load_reference(course):
    return pd.read_csv(f"data/{slug(course)}.csv")


META = load_meta()

# ============================================================
# 3. HELPER FUNCTIONS
# ============================================================

LABEL_STYLE = {
    "Good": ("good", "#22e58b"),
    "Average": ("avg", "#f5a524"),
    "Needs Improvement": ("bad", "#f43f5e"),
}


def label_from_percentile(pct):
    """Dataset ke students ke hisab se: neeche 35% = low, upar 30% = good."""
    if pct < 35:
        return "Needs Improvement"
    if pct < 70:
        return "Average"
    return "Good"


def donut(value, color):
    fig = go.Figure(go.Pie(
        values=[value, 100 - value], hole=0.75, sort=False, textinfo="none", hoverinfo="skip",
        marker=dict(colors=[color, "rgba(255,255,255,0.08)"])))
    fig.update_layout(
        showlegend=False, height=130, margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(text=f"{value:.0f}", x=0.5, y=0.5, showarrow=False,
                          font=dict(size=20, color="white"))])
    return fig


def analyze(course, marks, hours):
    meta = META[course]
    ref = load_reference(course)
    models = load_models(course)

    values = dict(marks)
    values["study_hours"] = hours

    info = {}
    for s in meta["subjects"]:
        feats = meta["features"][s]
        row = pd.DataFrame([[values[f] for f in feats]], columns=feats)
        expected = float(models[s].predict(row)[0])
        pct = float((ref[s] < marks[s]).mean() * 100)
        target = min(100.0, max(marks[s] + 5, float(ref[s].quantile(0.70))))
        info[s] = {
            "expected": expected,
            "percentile": pct,
            "label": label_from_percentile(pct),
            "target": target,
            "need": max(0.0, target - marks[s]),
        }

    overall = sum(marks.values()) / len(marks)
    ref_overall = ref[meta["subjects"]].mean(axis=1)
    overall_pct = float((ref_overall < overall).mean() * 100)
    return info, overall, overall_pct, label_from_percentile(overall_pct)


def hours_split(info, total_hours):
    """Weak subject ko zyada time."""
    weight = {"Needs Improvement": 3, "Average": 2, "Good": 1}
    total_w = sum(weight[v["label"]] for v in info.values())
    total_hours = max(total_hours, 1.0)
    return {s: total_hours * weight[v["label"]] / total_w for s, v in info.items()}


def make_plan(info, split):
    order = sorted(info, key=lambda s: info[s]["percentile"])
    a, b, c = order[0], order[1], order[2]
    return [
        f"Day 1: **{a}** ke basic concepts revise karo ({split[a]:.1f} h)",
        f"Day 2: **{a}** ke practice questions solve karo ({split[a]:.1f} h)",
        f"Day 3: **{b}** ka weak part revise karo ({split[b]:.1f} h)",
        f"Day 4: **{a}** aur **{b}** ka mini test do",
        f"Day 5: **{c}** revise karo + **{b}** ke questions solve karo",
        "Day 6: Sab subjects ke previous year questions solve karo",
        "Day 7: Full mock test do aur galtiyan note karo",
    ]


# ============================================================
# 4. SIDEBAR + HEADER
# ============================================================

with st.sidebar:
    st.markdown("<div class='brand'>"
                "<div class='brand-icon'>🎓</div>"
                "<div class='brand-name'>StudyMate</div>"
                "<div class='brand-tagline'>Predict • Analyze • Improve</div>"
                "</div>",
                unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**🏠 Dashboard**")
    st.markdown("📅 Study Planner")
    st.markdown("📊 Analytics")
    st.markdown("ℹ️ About")
    st.markdown("---")
    st.markdown("🚀 **Dream Big, Study Smart!**")

st.markdown("<header class='page-header'>"
            "<h1>Student Performance Dashboard</h1>"
            "<p>Analyze marks, compare progress, and receive a personalized study plan.</p>"
            "</header>",
            unsafe_allow_html=True)

left, right = st.columns([1, 2.4], gap="medium")

# ============================================================
# 5. LEFT PANEL (course -> subjects badal jaate hain)
# ============================================================

with left:
    with st.container(border=True):
        st.markdown("<div class='card-title'>👤 Student Details & Marks</div>", unsafe_allow_html=True)
        sid = st.text_input("Student ID", "STU2026001")
        name = st.text_input("Name", "Md Danish Ali")
        course = st.selectbox("Course", list(META.keys()))

        subjects = META[course]["subjects"]
        ref = load_reference(course)

        st.caption(f"Subjects are updated based on your course  |  Total Subjects: {len(subjects)}")

        marks = {}
        cols = st.columns(3)
        for i, s in enumerate(subjects):
            marks[s] = cols[i % 3].number_input(
                s, 0, 100, int(round(ref[s].mean())), key=f"{course}_{s}")

        hours = st.slider("Daily Study Hours", 0.5, 8.0, 3.0, 0.5)

        if st.button("✨ Analyze Performance  →", use_container_width=True):
            st.session_state["ran"] = True

if not st.session_state.get("ran"):
    with right:
        st.markdown("<div class='empty-state'>"
                    "<div class='empty-state-icon'>📊</div>"
                    "<strong>Ready to analyze performance?</strong>"
                    "<p>Select a course, enter the marks, and choose<br><b>Analyze Performance</b>.</p>"
                    "</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# 6. ANALYSIS
# ============================================================

info, overall, overall_pct, overall_label = analyze(course, marks, hours)
split = hours_split(info, hours)
plan = make_plan(info, split)

best = max(subjects, key=lambda s: marks[s])
worst = min(subjects, key=lambda s: info[s]["percentile"])
low_subjects = [s for s in subjects if info[s]["label"] == "Needs Improvement"]
avg_subjects = [s for s in subjects if info[s]["label"] == "Average"]
below_expected = [s for s in subjects if marks[s] < info[s]["expected"] - 5]
hero_color = LABEL_STYLE[overall_label][1]

# ============================================================
# 7. RIGHT PANEL
# ============================================================

with right:
    st.markdown(
        "<div class='hero'><div>"
        "<span class='pill'>✅ Prediction Result</span>"
        f"<div style='margin-top:10px;font-size:20px;font-weight:700'>{name}, your overall performance is</div>"
        f"<div class='big' style='color:{hero_color}'>{overall_label}</div>"
        f"<div style='margin-top:8px'>Estimated Score: <span class='green'>{overall:.1f}%</span>"
        f" &nbsp;|&nbsp; Better than <span class='green'>{overall_pct:.0f}%</span> {course} students in dataset</div>"
        "</div><div style='font-size:90px'>🏆</div></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<div class='card-title'>📈 Subject-wise Analysis</div>", unsafe_allow_html=True)
        cols = st.columns(len(subjects))
        for col, s in zip(cols, subjects):
            css, color = LABEL_STYLE[info[s]["label"]]
            with col:
                st.markdown(f"<div class='subname'>{s}</div>", unsafe_allow_html=True)
                st.plotly_chart(donut(marks[s], color), use_container_width=True,
                                config={"displayModeBar": False}, key=f"d_{course}_{s}")
                st.markdown(
                    f"<div style='text-align:center'><span class='tag {css}'>{info[s]['label']}</span>"
                    f"<div class='muted'>Expected: {info[s]['expected']:.0f}<br>"
                    f"Top {100 - info[s]['percentile']:.0f}%</div></div>", unsafe_allow_html=True)

# ============================================================
# 8. BOTTOM CARDS
# ============================================================

b1, b2, b3 = st.columns([1.3, 1, 1], gap="medium")

with b1:
    with st.container(border=True):
        st.markdown("<div class='card-title'>🎯 Personalized Study Plan "
                    "<span class='tag good'>7 Days</span></div>", unsafe_allow_html=True)
        st.markdown(f"Focus more on: <span class='green'>{worst}</span> "
                    f"(Need +{info[worst]['need']:.0f} marks, target {info[worst]['target']:.0f})",
                    unsafe_allow_html=True)
        st.markdown("**Daily time split:**")
        for s in sorted(subjects, key=lambda x: info[x]["percentile"])[:3]:
            st.markdown(f"✅ {s}: {split[s]:.1f} h/day")
        with st.expander("View Full Study Plan →"):
            for item in plan:
                st.markdown(f"✅ {item}")

with b2:
    with st.container(border=True):
        st.markdown("<div class='card-title'>💡 Key Insights</div>", unsafe_allow_html=True)
        st.markdown(
            f"🏆 Best Subject: **{best} ({marks[best]})**<br><br>"
            f"⚠️ Weakest Subject: **{worst} ({marks[worst]})**<br><br>"
            f"🔴 Low: **{', '.join(low_subjects) if low_subjects else 'None'}**<br><br>"
            f"🟠 Average: **{', '.join(avg_subjects) if avg_subjects else 'None'}**<br><br>"
            f"📉 Below expected: **{', '.join(below_expected) if below_expected else 'None'}**<br><br>"
            f"⭐ Overall Strength: **{overall_label}**", unsafe_allow_html=True)

with b3:
    with st.container(border=True):
        st.markdown("<div class='card-title'>🛠️ Next Steps</div>", unsafe_allow_html=True)
        weak_names = ", ".join((low_subjects or avg_subjects)[:2]) or "all subjects"
        st.markdown(
            f"**1.** Focus on weak subjects: **{weak_names}**<br><br>"
            "**2.** Take mock tests regularly<br><br>"
            "**3.** Improve core concepts<br><br>"
            "**4.** Track your progress weekly", unsafe_allow_html=True)