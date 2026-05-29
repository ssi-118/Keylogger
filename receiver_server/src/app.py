import json
import os
from datetime import datetime, timezone
from pathlib import Path

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

LOG_FILE = DATA_DIR / "encrypted_logs.jsonl"

FERNET_KEY = os.getenv("FERNET_KEY")
API_TOKEN = os.getenv("API_TOKEN")

if not FERNET_KEY:
    raise RuntimeError("Missing FERNET_KEY in .env")

if not API_TOKEN:
    raise RuntimeError("Missing API_TOKEN in .env")

fernet = Fernet(FERNET_KEY.encode())


def is_authorized(req):
    return req.headers.get("X-API-Token") == API_TOKEN


@app.get("/")
def health_check():
    return jsonify({
        "service": "Remote Logging Receiver",
        "status": "running",
    })


@app.post("/api/remote-log")
def remote_log():
    if not is_authorized(request):
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": payload.get("source", "typing_client"),
        "event_type": "consented_typing_sample",
        "text": text,
        "length": len(text),
    }

    encrypted = fernet.encrypt(json.dumps(record).encode()).decode()

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps({"encrypted": encrypted}) + "\n")

    return jsonify({
        "status": "stored",
        "encrypted": True,
        "ciphertext": encrypted,
    })


@app.get("/api/logs")
def logs():
    if not is_authorized(request):
        return jsonify({"error": "Unauthorized"}), 401

    if not LOG_FILE.exists():
        return jsonify({"count": 0, "logs": []})

    logs_list = []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            encrypted_item = json.loads(line)
            decrypted = fernet.decrypt(encrypted_item["encrypted"].encode())

            logs_list.append({
                "encrypted": encrypted_item["encrypted"],
                "decrypted": json.loads(decrypted),
            })

    return jsonify({
        "count": len(logs_list),
        "logs": logs_list[-10:],
    })


@app.post("/api/clear")
def clear_logs():
    if not is_authorized(request):
        return jsonify({"error": "Unauthorized"}), 401

    LOG_FILE.write_text("", encoding="utf-8")
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 7000))
    app.run(host="0.0.0.0", port=port, debug=False)