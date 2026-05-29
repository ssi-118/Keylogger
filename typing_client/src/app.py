import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)

REMOTE_SERVER_URL = os.getenv("REMOTE_SERVER_URL")
API_TOKEN = os.getenv("API_TOKEN")

if not REMOTE_SERVER_URL:
    raise RuntimeError("Missing REMOTE_SERVER_URL in .env")

if not API_TOKEN:
    raise RuntimeError("Missing API_TOKEN in .env")


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/send")
def send():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")

    response = requests.post(
        f"{REMOTE_SERVER_URL}/api/remote-log",
        headers={"X-API-Token": API_TOKEN},
        json={
            "source": "student_typing_client",
            "text": text,
        },
        timeout=10,
    )

    return jsonify(response.json()), response.status_code


@app.get("/logs")
def logs():
    response = requests.get(
        f"{REMOTE_SERVER_URL}/api/logs",
        headers={"X-API-Token": API_TOKEN},
        timeout=10,
    )

    return jsonify(response.json()), response.status_code


@app.post("/clear")
def clear():
    response = requests.post(
        f"{REMOTE_SERVER_URL}/api/clear",
        headers={"X-API-Token": API_TOKEN},
        timeout=10,
    )

    return jsonify(response.json()), response.status_code


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)