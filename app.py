"""
app.py — Flask entry point for AI StudyMate
Run: python app.py
"""
import os
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException
from routes.api import api

app = Flask(__name__)
app.register_blueprint(api)


@app.errorhandler(Exception)
def handle_server_error(error):
    if isinstance(error, HTTPException):
        return {"error": error.description}, error.code
    app.logger.exception("Unhandled application error")
    return {"error": "The server encountered an unexpected error. Please try again."}, 500


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # Bind on all interfaces so the app also works through VS Code port forwarding.
    app.run(host="0.0.0.0", port=5000, debug=False)
