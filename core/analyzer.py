"""
core/analyzer.py
Pure analysis logic — no UI code. Called by routes/api.py.
"""
import pandas as pd
from .model_loader import get_meta, get_models, get_reference


def label_from_percentile(pct):
    """Map a percentile score to a human-readable performance label."""
    if pct < 35:
        return "Needs Improvement"
    if pct < 70:
        return "Average"
    return "Good"


def analyze(course, marks, hours):
    """
    Run ML prediction + percentile calculation for every subject.

    Parameters
    ----------
    course : str   e.g. "BCA"
    marks  : dict  {subject: float_score}
    hours  : float daily study hours

    Returns
    -------
    info         : dict  per-subject stats
    overall      : float mean score
    overall_pct  : float percentile vs reference dataset
    overall_label: str   label for overall percentile
    """
    meta = get_meta()
    ref = get_reference(course)
    models = get_models(course)
    subjects = meta[course]["subjects"]

    values = dict(marks)
    values["study_hours"] = hours

    info = {}
    for s in subjects:
        feats = meta[course]["features"][s]
        row = pd.DataFrame([[values[f] for f in feats]], columns=feats)
        expected = float(models[s].predict(row)[0])
        pct = float((ref[s] < marks[s]).mean() * 100)
        target = min(100.0, max(marks[s] + 5, float(ref[s].quantile(0.70))))
        info[s] = {
            "expected": round(expected, 1),
            "percentile": round(pct, 1),
            "label": label_from_percentile(pct),
            "target": round(target, 1),
            "need": round(max(0.0, target - marks[s]), 1),
        }

    overall = sum(marks.values()) / len(marks)
    ref_overall = ref[subjects].mean(axis=1)
    overall_pct = float((ref_overall < overall).mean() * 100)
    return (
        info,
        round(overall, 1),
        round(overall_pct, 1),
        label_from_percentile(overall_pct),
    )


def hours_split(info, total_hours):
    """
    Distribute daily study hours across subjects.
    Weak subjects receive proportionally more time.
    """
    weight = {"Needs Improvement": 3, "Average": 2, "Good": 1}
    total_w = sum(weight[v["label"]] for v in info.values())
    total_hours = max(total_hours, 1.0)
    return {
        s: round(total_hours * weight[v["label"]] / total_w, 1)
        for s, v in info.items()
    }


def make_plan(info, split):
    """Generate a 7-day personalised study plan."""
    order = sorted(info, key=lambda s: info[s]["percentile"])
    a = order[0]
    b = order[1] if len(order) > 1 else order[0]
    c = order[2] if len(order) > 2 else order[0]
    return [
        f"Day 1: {a} — Revise basic concepts ({split[a]} h)",
        f"Day 2: {a} — Solve practice questions ({split[a]} h)",
        f"Day 3: {b} — Revise weak areas ({split[b]} h)",
        f"Day 4: {a} & {b} — Mini test",
        f"Day 5: {c} — Revise + {b} — Practice questions",
        "Day 6: Solve previous year questions for all subjects",
        "Day 7: Full mock test — Review mistakes",
    ]
