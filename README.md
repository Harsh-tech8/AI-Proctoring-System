# AI Proctoring System

A production-style starter architecture for an AI-assisted online exam proctoring system.

## Architecture

```text
Candidate Browser
      |
      v
 Gateway (FastAPI :8000)
      |
      | Redis Streams
      v
 Vision Worker (OpenCV)
      |
      | anti-cheat events
      v
 Scoring Engine
      |
      v
 Redis + Proctor Dashboard
```

### Detection signals

The OpenCV engine currently detects:

- `NO_FACE` — no face visible
- `MULTIPLE_FACES` — more than one face visible
- `LOOKING_AWAY` — face/eye region suggests gaze divergence
- `CAMERA_ERROR` — camera frame could not be processed

This is an AI-assisted signal system, not a definitive cheating verdict. Events are scored and shown to a human proctor for review.

## Project structure

```text
ai-proctoring-system/
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .gitignore
├── Makefile
├── requirements.txt
├── README.md
├── scripts/
│   ├── generate_zip.py
│   └── healthcheck.py
├── services/
│   ├── gateway/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       └── schemas.py
│   ├── vision_worker/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── detector.py
│   │       └── worker.py
│   └── scoring_engine/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── app/
│           ├── __init__.py
│           └── worker.py
└── web/
    ├── candidate/
    │   ├── index.html
    │   ├── app.js
    │   └── style.css
    └── proctor/
        ├── index.html
        ├── app.js
        └── style.css
```

## Run with Docker

1. Install Docker Desktop.
2. Open a terminal in this folder.
3. Copy `.env.example` to `.env`.
4. Run:

```bash
docker compose up --build
```

5. Candidate page:

```text
http://localhost:8000
```

6. Proctor dashboard:

```text
http://localhost:8000/proctor
```

7. API health:

```text
http://localhost:8000/health
```

## Run locally without Docker

Python 3.10 or 3.11 is recommended for the easiest OpenCV setup.

Install:

```bash
pip install -r requirements.txt
```

Start Redis separately, then start each service using its service requirements.

## Important production notes

Before using this with real candidates:

- Add authentication and authorization.
- Use HTTPS.
- Store only necessary video/event data.
- Add consent and privacy notices.
- Encrypt sensitive data.
- Add rate limits.
- Add structured logging and monitoring.
- Calibrate gaze detection for different cameras and lighting.
- Test false-positive/false-negative rates.
- Never make an automatic accusation solely from an AI signal.
