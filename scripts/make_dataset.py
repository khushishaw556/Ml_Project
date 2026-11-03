# ============================================================
# STEP 1: make_dataset.py
# Course-wise student marks dataset banata hai (data/ folder mein)
# Run:  python make_dataset.py
#
# NOTE: Ye SYNTHETIC (banaya hua) sample data hai, kyunki Kaggle par
# BCA/BTech ke subject-wise marks ka dataset nahi milta.
# Baad mein is data ko apne classmates ke asli marks se badal sakte ho:
# bas data/BCA.csv jaisi file ka format same rakho
# (student_id, 6 subject columns, study_hours).
# ============================================================

import os
import numpy as np
import pandas as pd

np.random.seed(42)

COURSES = {
    "BCA": ["Java", "Operating System", "Machine Learning",
            "Computer Networks", "HTML & CSS", "DBMS"],
    "BTech CSE": ["DSA", "Operating System", "DBMS",
                  "Computer Networks", "Python", "Engineering Maths"],
    "MCA": ["Advanced Java", "Cloud Computing", "Data Science",
            "Software Engineering", "Web Technologies", "Algorithms"],
}

N = 1000  # students per course

os.makedirs("data", exist_ok=True)

for course, subjects in COURSES.items():

    # Har student ki ek general ability (achha student -> sab subjects mein thoda achha)
    ability = np.random.normal(0, 1, N)

    # Study hours bhi ability se thode related
    study = np.clip(
        np.round(3 + 0.8 * ability + np.random.normal(0, 1.2, N), 1),
        0.5, 8
    )

    data = {
        "student_id": [f"{course[:3].upper()}{i:04d}" for i in range(1, N + 1)]
    }

    for subject in subjects:
        base = np.random.uniform(58, 72)       # subject ki average difficulty
        loading = np.random.uniform(8, 13)     # ability ka asar
        noise = np.random.uniform(6, 10)       # subject-specific randomness

        marks = (
            base
            + loading * ability
            + 1.5 * (study - 3)                # zyada padhai -> thode zyada marks
            + np.random.normal(0, noise, N)
        )
        data[subject] = np.clip(np.round(marks), 20, 100).astype(int)

    data["study_hours"] = study

    df = pd.DataFrame(data)
    path = f"data/{course.replace(' ', '_')}.csv"
    df.to_csv(path, index=False)

    print(f"{course}: {df.shape[0]} students -> {path}")

print("\nDone! Ab 'python train_courses.py' chalao.")