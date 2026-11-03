"""
routes/api.py
Flask Blueprint exposing:
  GET  /api/courses   → course → subjects mapping
  POST /api/analyze   → full analysis payload
"""
from flask import Blueprint, request, jsonify
from core.model_loader import get_meta
from core.analyzer import analyze, hours_split, make_plan
from core.resources import get_recommended_resources

api = Blueprint("api", __name__)


@api.route("/api/courses")
def courses():
    """Return all available courses and their subjects."""
    meta = get_meta()
    result = {course: info["subjects"] for course, info in meta.items()}
    return jsonify(result)


@api.route("/api/analyze", methods=["POST"])
def analyze_route():
    """
    Accept JSON body:
      { course, marks: {subject: score}, hours, name }
    Return full analysis result as JSON.
    """
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    course = data.get("course")
    meta = get_meta()
    if course not in meta:
        return jsonify({"error": "Please select a valid course."}), 400

    marks_data = data.get("marks")
    if not isinstance(marks_data, dict):
        return jsonify({"error": "Marks must be provided for every subject."}), 400

    subjects = meta[course]["subjects"]
    missing = [subject for subject in subjects if subject not in marks_data]
    if missing:
        return jsonify({"error": f"Missing marks for: {', '.join(missing)}"}), 400

    try:
        marks = {subject: float(marks_data[subject]) for subject in subjects}
        hours = float(data.get("hours", 3.0))
    except (TypeError, ValueError):
        return jsonify({"error": "Marks and study hours must be numeric."}), 400

    if any(mark < 0 or mark > 100 for mark in marks.values()):
        return jsonify({"error": "Each mark must be between 0 and 100."}), 400
    if hours < 1 or hours > 24:
        return jsonify({"error": "Study hours must be between 1 and 24."}), 400

    student_name = str(data.get("name", "Student")).strip() or "Student"
    info, overall, overall_pct, overall_label = analyze(course, marks, hours)
    split = hours_split(info, hours)
    plan = make_plan(info, split)
    best = max(subjects, key=lambda s: marks[s])
    worst = min(subjects, key=lambda s: info[s]["percentile"])
    low_subjects = [s for s in subjects if info[s]["label"] == "Needs Improvement"]
    avg_subjects = [s for s in subjects if info[s]["label"] == "Average"]
    below_expected = [s for s in subjects if marks[s] < info[s]["expected"] - 5]

    return jsonify(
        {
            "name": student_name,
            "course": course,
            "overall": overall,
            "overall_pct": overall_pct,
            "overall_label": overall_label,
            "subjects": subjects,
            "marks": marks,
            "info": info,
            "split": split,
            "plan": plan,
            "best": best,
            "worst": worst,
            "low_subjects": low_subjects,
            "avg_subjects": avg_subjects,
            "below_expected": below_expected,
            "recommended_resources": get_recommended_resources(info, marks),
        }
    )
