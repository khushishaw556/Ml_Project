# ============================================================
# STEP 2: train_courses.py
# data/ ki har course file se har subject ke liye model train karta hai
# Run:  python train_courses.py
# pip install pandas numpy matplotlib seaborn scikit-learn joblib
# ============================================================

import os
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # graphs sirf save honge (window nahi khulegi)
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

os.makedirs("models", exist_ok=True)
os.makedirs("graphs", exist_ok=True)

meta = {}
all_results = []

for file in sorted(os.listdir("data")):

    if not file.endswith(".csv"):
        continue

    course = file.replace(".csv", "").replace("_", " ")
    slug = file.replace(".csv", "")

    # ------------------------------------------------------------
    # 1. Load + clean
    # ------------------------------------------------------------
    df = pd.read_csv(f"data/{file}")
    df = df.drop_duplicates()

    subjects = [c for c in df.columns if c not in ("student_id", "study_hours")]

    for c in subjects + ["study_hours"]:
        df[c] = df[c].fillna(df[c].mean())

    print("\n========================================")
    print("COURSE:", course, "| Students:", len(df))
    print("Subjects:", subjects)

    # ------------------------------------------------------------
    # 2. EDA graph (correlation heatmap)
    # ------------------------------------------------------------
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[subjects + ["study_hours"]].corr(), annot=True, cmap="coolwarm")
    plt.title(f"Correlation Heatmap - {course}")
    plt.tight_layout()
    plt.savefig(f"graphs/heatmap_{slug}.png")
    plt.close()

    # ------------------------------------------------------------
    # 3. Train: har subject = baaki subjects + study_hours se predict
    # ------------------------------------------------------------
    meta[course] = {"subjects": subjects, "features": {}, "files": {}}

    for i, target in enumerate(subjects):

        features = [s for s in subjects if s != target] + ["study_hours"]

        X = df[features]
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        candidates = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        }

        best_r2 = -999
        best_name, best_model = None, None

        for name, model in candidates.items():
            model.fit(X_train, y_train)
            pred = model.predict(X_test)

            r2 = r2_score(y_test, pred)
            mae = mean_absolute_error(y_test, pred)

            all_results.append({
                "Course": course, "Subject": target, "Model": name,
                "R2": round(r2, 4), "MAE": round(mae, 2),
            })

            if r2 > best_r2:
                best_r2, best_name, best_model = r2, name, model

        path = f"models/{slug}_{i}.pkl"
        joblib.dump(best_model, path)

        meta[course]["features"][target] = features
        meta[course]["files"][target] = path

        print(f"  {target}: best = {best_name} (R2 = {best_r2:.3f})")

# ------------------------------------------------------------
# 4. Evaluation table + graph (report ke liye)
# ------------------------------------------------------------
results_df = pd.DataFrame(all_results)

print("\n========================================")
print("MODEL EVALUATION")
print("========================================")
print(results_df.to_string(index=False))

results_df.to_csv("graphs/model_evaluation.csv", index=False)

plt.figure(figsize=(10, 5))
sns.barplot(data=results_df, x="Course", y="R2", hue="Model")
plt.title("Model Comparison (R2 Score) by Course")
plt.tight_layout()
plt.savefig("graphs/model_comparison.png")
plt.close()

joblib.dump(meta, "meta.pkl")

print("\nSaved: models/, meta.pkl, graphs/")
print("Ab chalao: python -m streamlit run studymates_v2.py")