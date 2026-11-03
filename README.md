# 🎓 AI StudyMate — Flask Web App

An AI-powered student performance dashboard that predicts subject-wise scores, computes percentile ranks against a reference dataset, and generates a personalised 7-day study plan.

---

## 📁 Folder Structure

```
ai_studymates/
├── app.py                    # Flask entry point
├── requirements.txt
├── README.md
│
├── core/                     # Pure Python logic (no UI)
│   ├── __init__.py
│   ├── model_loader.py       # Load meta.pkl + per-course models
│   ├── analyzer.py           # analyze(), hours_split(), make_plan()
│   └── resources.py          # Curated learning resources based on performance
│
├── routes/                   # Flask Blueprints
│   ├── __init__.py
│   └── api.py                # GET /api/courses, POST /api/analyze
│
├── static/
│   ├── css/style.css         # All custom CSS (dark-navy theme)
│   ├── js/app.js             # Vanilla JS frontend logic
│   └── img/                  # (reserved for future assets)
│
├── templates/
│   └── index.html            # Single-page HTML app
│
├── scripts/                  # Data generation & training scripts
│   ├── make_dataset.py       # Generate synthetic CSV data
│   └── train_courses.py      # Train ML models, save meta.pkl
│
├── data/                     # BCA.csv, BTech_CSE.csv, MCA.csv
├── models/                   # BCA_0.pkl … MCA_5.pkl
└── meta.pkl                  # Course metadata (subjects, features, model paths)
```

---

## ⚙️ Setup

### 1. Clone / navigate to the project

```bash
cd d:\ai_studymates
```

### 2. Create & activate a virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate synthetic data (skip if `data/` already exists)

```bash
python scripts/make_dataset.py
```

### 5. Train models (skip if `models/` and `meta.pkl` already exist)

```bash
python scripts/train_courses.py
```

---

## 🚀 Run the App

```bash
python app.py
```

Open your browser at → **http://localhost:5000**

> The Flask dev server runs in debug mode on port 5000 by default.

---

## 🌐 API Reference

| Method | Endpoint       | Description                              |
|--------|---------------|------------------------------------------|
| GET    | `/api/courses` | Returns all courses and their subjects   |
| POST   | `/api/analyze` | Runs analysis; returns full result JSON  |

### POST `/api/analyze` — request body

```json
{
  "name":   "Md Danish Ali",
  "course": "BCA",
  "marks":  { "Java": 75, "Operating System": 60, "..." : 0 },
  "hours":  3.0
}
```

---

## 🛠️ Re-training Models

If you update the data CSVs, re-run the training pipeline from the project root:

```bash
python scripts/make_dataset.py   # regenerate data/
python scripts/train_courses.py  # retrain and overwrite models/ + meta.pkl
```

---

## 📦 Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python 3.10+, Flask 3             |
| ML         | scikit-learn, joblib, pandas      |
| Frontend   | Vanilla HTML5 / CSS3 / JavaScript |
| Fonts      | Inter (Google Fonts)              |

---

> **Dream Big, Study Smart! 🚀**
