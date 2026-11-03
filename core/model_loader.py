"""
core/model_loader.py
Loads meta.pkl and per-course ML models. Paths resolve relative to project root.
"""
import os
import joblib
import pandas as pd

_META = None
_MODELS_CACHE = {}

# Project root = one level above this file (core/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_meta():
    global _META
    if _META is None:
        _META = joblib.load(os.path.join(BASE_DIR, "meta.pkl"))
    return _META


def get_models(course):
    if course not in _MODELS_CACHE:
        meta = get_meta()
        _MODELS_CACHE[course] = {
            s: joblib.load(p) for s, p in meta[course]["files"].items()
        }
    return _MODELS_CACHE[course]


def get_reference(course):
    meta = get_meta()
    slug = course.replace(" ", "_")
    path = os.path.join(BASE_DIR, "data", f"{slug}.csv")
    return pd.read_csv(path)
