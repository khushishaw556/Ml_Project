# ============================================================
# AI STUDYMATE - TRAINING FILE (train.py)
# Dataset: StudentsPerformance.csv (Kaggle)
# Run:  python train.py
# pip install pandas numpy matplotlib seaborn scikit-learn joblib
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

os.makedirs("graphs", exist_ok=True)

# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv("StudentsPerformance.csv")

# Make column names simple: "math score" -> "math_score"
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(r"[ /]", "_", regex=True)
)

print("\n========================================")
print("DATASET")
print("========================================")
print(df.head())
print("\nColumns:", list(df.columns))
print("Shape:", df.shape)

SUBJECTS = ["math_score", "reading_score", "writing_score"]

# ============================================================
# 2. DATA CLEANING
# ============================================================

print("\n========================================")
print("DATA CLEANING")
print("========================================")

print("Missing values:\n", df.isnull().sum())
print("Duplicate rows:", df.duplicated().sum())

df = df.drop_duplicates()

for col in SUBJECTS:
    df[col] = df[col].fillna(df[col].mean())

# Encode test preparation course: completed = 1, none = 0
df["test_prep"] = (df["test_preparation_course"] == "completed").astype(int)

df["overall_score"] = df[SUBJECTS].mean(axis=1)

print("Cleaning done. Shape:", df.shape)

# ============================================================
# 3. EDA (graphs are also saved in /graphs for your report)
# ============================================================

print("\n========================================")
print("EDA")
print("========================================")
print(df[SUBJECTS + ["overall_score"]].describe())

# Graph 1: Score distribution of 3 subjects
plt.figure(figsize=(9, 5))
for col in SUBJECTS:
    plt.hist(df[col], bins=20, alpha=0.5, label=col.replace("_score", ""))
plt.title("Score Distribution")
plt.xlabel("Marks")
plt.ylabel("Students")
plt.legend()
plt.tight_layout()
plt.savefig("graphs/1_distribution.png")
plt.show()

# Graph 2: Average score by test preparation
plt.figure(figsize=(7, 5))
df.groupby("test_preparation_course")[SUBJECTS].mean().plot(kind="bar")
plt.title("Average Marks by Test Preparation")
plt.ylabel("Average Marks")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("graphs/2_test_prep.png")
plt.show()

# Graph 3: Correlation heatmap
plt.figure(figsize=(7, 5))
sns.heatmap(df[SUBJECTS + ["test_prep"]].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("graphs/3_heatmap.png")
plt.show()

# ============================================================
# 4. TRAIN MODELS (one model per subject)
# Idea: predict "expected marks" of a subject using the OTHER
# subjects + test prep. If actual marks < expected, subject is weak.
# ============================================================

print("\n========================================")
print("MODEL TRAINING")
print("========================================")

results = []
best_models = {}
feature_map = {}

for target in SUBJECTS:

    others = [s for s in SUBJECTS if s != target]
    features = others + ["test_prep"]

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    candidates = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=100, random_state=42
        ),
    }

    best_r2 = -999

    for name, model in candidates.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        r2 = r2_score(y_test, pred)
        mae = mean_absolute_error(y_test, pred)

        results.append({
            "Subject": target,
            "Model": name,
            "R2": round(r2, 4),
            "MAE": round(mae, 2),
        })

        if r2 > best_r2:
            best_r2 = r2
            best_models[target] = (name, model)

    feature_map[target] = features

results_df = pd.DataFrame(results)

print("\n========================================")
print("MODEL EVALUATION")
print("========================================")
print(results_df.to_string(index=False))

# Graph 4: Model comparison
plt.figure(figsize=(9, 5))
sns.barplot(data=results_df, x="Subject", y="R2", hue="Model")
plt.title("Model Comparison (R2 Score)")
plt.tight_layout()
plt.savefig("graphs/4_model_comparison.png")
plt.show()

# ============================================================
# 5. SAVE EVERYTHING FOR THE UI
# ============================================================

print("\n========================================")
print("SAVING")
print("========================================")

for target, (name, model) in best_models.items():
    joblib.dump(model, f"model_{target}.pkl")
    print(f"{target}: best model = {name} -> model_{target}.pkl")

joblib.dump(feature_map, "feature_map.pkl")

# Reference marks (used for percentile in the UI)
df[SUBJECTS].to_csv("reference_marks.csv", index=False)

print("\nDone! Now build app.py")