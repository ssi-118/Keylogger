# TypeTrail Lab - Keylogger

TypeTrail Lab is a consent-based cybersecurity learning project that demonstrates remote logging, encryption, and API communication using Flask.

This is **not a background keylogger**. It only records text typed directly into the web page after the user gives consent.

## Features

- Consent-based typing sample collection
- Remote logging using two Flask apps
- Fernet encryption before storage
- API token protection between client and receiver
- Simple SaaS-style user interface
- Remote log viewing from the client website

## Project Structure

```text
KeyloggerRemoteLab/
  receiver_server/
    src/
      app.py
      generate_key.py
    data/
      encrypted_logs.jsonl
    requirements.txt
    .env.example

  typing_client/
    src/
      app.py
      templates/
        index.html
      static/
        app.js
        styles.css
    requirements.txt
    .env.example
```

## How It Works

```text
User opens typing_client
→ types a sample after consent
→ client sends sample to receiver_server
→ receiver encrypts and stores the log
→ client can fetch and display remote logs
```

## Setup

Clone the project:

```bash
git clone YOUR_REPO_URL
cd KeyloggerRemoteLab
```

## Start Receiver Server

```bash
cd receiver_server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/generate_key.py
```

Create a `.env` file:

```env
FERNET_KEY=paste_generated_key_here
API_TOKEN=student-demo-secret-token
```

Run the receiver:

```bash
python src/app.py
```

Receiver runs at:

```text
http://127.0.0.1:7000
```

## Start Typing Client

Open a second terminal:

```bash
cd typing_client
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
REMOTE_SERVER_URL=http://127.0.0.1:7000
API_TOKEN=student-demo-secret-token
```

Run the client:

```bash
python src/app.py
```

Client runs at:

```text
http://127.0.0.1:5000
```

Open this in your browser:

```text
http://127.0.0.1:5000
```

## Deployment

For Render, deploy two web services.

### Receiver Service

Root directory:

```text
receiver_server
```

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn src.app:app
```

Environment variables:

```env
FERNET_KEY=your_generated_fernet_key
API_TOKEN=your_shared_api_token
```

### Client Service

Root directory:

```text
typing_client
```

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn src.app:app
```

Environment variables:

```env
REMOTE_SERVER_URL=https://your-receiver-service.onrender.com
API_TOKEN=your_shared_api_token
```

## Important Notes

- Do not commit `.env` files.
- Do not commit `.venv` folders.
- Do not use this project for silent monitoring.
- This project is for ethical cybersecurity learning only.
- Only text typed into the visible webpage is recorded.

## Live Demo
```
https://keylogger-main-qrda.onrender.com
```
