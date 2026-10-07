<div align="center">

# ⚡ `AI PROCTORING SYSTEM`

### 🎌 **THE EXAMINATION SENTINEL**

<img src="https://img.shields.io/badge/STATUS-ACTIVE-00ff9d?style=for-the-badge" />
<img src="https://img.shields.io/badge/AI-COMPUTER%20VISION-9d4edd?style=for-the-badge" />
<img src="https://img.shields.io/badge/ARCHITECTURE-MICROSERVICES-ff6b6b?style=for-the-badge" />
<img src="https://img.shields.io/badge/POWERED%20BY-PYTHON-3776AB?style=for-the-badge" />

<br>

### 👁️ **"The camera sees. The AI analyzes. The human decides."**

</div>

---

# 🌌 `01` — ENTER THE SYSTEM

> **Welcome, Candidate.**

In a normal online examination...

```text
                 👨‍🎓
                 │
                 ▼
          ┌─────────────┐
          │   ONLINE    │
          │    EXAM     │
          └─────────────┘
                 │
                 ▼
              🤔
        "Who's watching?"
```

### Now imagine this...

```text
                         👁️
                         │
                         ▼
              ┌───────────────────┐
              │   AI SENTINEL     │
              │                   │
              │   👁️  👁️  👁️    │
              │                   │
              │   WATCHING...     │
              └─────────┬─────────┘
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
          🙂 NORMAL   👥 ALERT   ❌ ERROR
```

This project creates an **AI-assisted online examination monitoring system** capable of analyzing a candidate's camera feed and detecting unusual visual signals in real time.

---

# 🌀 `02` — THE STORY

Imagine the system as an anime squad.

Every character has one mission.

```text
                 🌌 THE PROCTOR SQUAD 🌌

                       👁️
                 ┌─────────────┐
                 │  VISION AI  │
                 │  "Observer" │
                 └──────┬──────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │                               │
        │        ⚡ CORE SYSTEM ⚡       │
        │                               │
        └───────────────────────────────┘
            ▲            ▲            ▲
            │            │            │
        🚪 GATE       🔴 REDIS      ⚖️ SCORE
       "Gateway"      "Messenger"    "Judge"
            │
            ▼
         🧑‍🎓
       CANDIDATE
```

### 🎭 The Characters

| Character         | Role                          |
| ----------------- | ----------------------------- |
| 🧑‍🎓 Candidate   | Takes the examination         |
| 🚪 Gateway        | Controls communication        |
| 👁️ Vision Worker | Watches and analyzes frames   |
| 🔴 Redis          | Moves events between services |
| ⚖️ Scoring Engine | Calculates risk information   |
| 🧑‍💼 Proctor     | Reviews the generated alerts  |

---

# ⚔️ `03` — MISSION

### 🎯 Primary Mission

Build a real-time AI-assisted system that can:

```text
📷 Capture
     ↓
🧠 Analyze
     ↓
🚨 Detect
     ↓
📊 Score
     ↓
👨‍💼 Review
```

### The system currently looks for:

```text
┌────────────────────────────────────────┐
│                                        │
│  🚫 NO_FACE                            │
│  No face visible in the camera frame   │
│                                        │
│  👥 MULTIPLE_FACES                     │
│  More than one face detected           │
│                                        │
│  👀 LOOKING_AWAY                       │
│  Possible gaze divergence detected     │
│                                        │
│  📷 CAMERA_ERROR                       │
│  Camera frame could not be processed   │
│                                        │
└────────────────────────────────────────┘
```

---

# 🧬 `04` — SYSTEM DNA

```text
                     ┌───────────────┐
                     │ 🧑‍🎓 CANDIDATE │
                     └───────┬───────┘
                             │
                             │ Camera
                             ▼
                   ┌──────────────────┐
                   │   🌐 WEB APP     │
                   └────────┬─────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ 🚪 FASTAPI GATEWAY │
                  └─────────┬──────────┘
                            │
                            │ Event Stream
                            ▼
                  ┌────────────────────┐
                  │ 🔴 REDIS STREAM    │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ 👁️ VISION WORKER  │
                  │      OpenCV        │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ ⚠️ DETECTION EVENT │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ ⚖️ SCORING ENGINE  │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ 🔴 REDIS STORAGE   │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ 🧑‍💼 PROCTOR PANEL │
                  └────────────────────┘
```

---

# 🏯 `05` — THE KINGDOM

## 📂 Complete Project Structure

```text
AI-PROCTORING-SYSTEM/
│
├── ⚙️ docker-compose.yml
├── 🐳 Dockerfile
├── 🔐 .env.example
├── 🚫 .gitignore
├── 🛠️ Makefile
├── 📦 requirements.txt
├── 📖 README.md
│
├── 📜 scripts/
│   │
│   ├── 📦 generate_zip.py
│   └── ❤️ healthcheck.py
│
├── ⚔️ services/
│   │
│   ├── 🚪 gateway/
│   │   ├── 🐳 Dockerfile
│   │   ├── 📦 requirements.txt
│   │   │
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── ⚡ main.py
│   │       └── 📋 schemas.py
│   │
│   ├── 👁️ vision_worker/
│   │   ├── 🐳 Dockerfile
│   │   ├── 📦 requirements.txt
│   │   │
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── 👁️ detector.py
│   │       └── ⚙️ worker.py
│   │
│   └── ⚖️ scoring_engine/
│       ├── 🐳 Dockerfile
│       ├── 📦 requirements.txt
│       │
│       └── app/
│           ├── __init__.py
│           └── ⚖️ worker.py
│
└── 🌐 web/
    │
    ├── 🧑‍🎓 candidate/
    │   ├── index.html
    │   ├── app.js
    │   └── style.css
    │
    └── 🧑‍💼 proctor/
        ├── index.html
        ├── app.js
        └── style.css
```

---

# 🧩 `06` — KNOW YOUR CHARACTERS

## 🚪 GATEWAY

### `services/gateway/`

**Codename:** `THE GATEKEEPER`

```text
        🌐 WORLD
           │
           ▼
    ┌──────────────┐
    │   GATEWAY    │
    │      🚪      │
    └──────┬───────┘
           │
      ┌────┴────┐
      ▼         ▼
   ACCEPT      REJECT
```

The Gateway is the main entry point.

It is built using **FastAPI**.

It handles:

```text
✓ Session creation
✓ Camera frame reception
✓ Frame validation
✓ Redis communication
✓ Alert retrieval
✓ Session retrieval
✓ Health checking
✓ Web page serving
```

---

# ⚡ `07` — THE COMMAND CENTER

## `main.py`

This is the heart of the Gateway.

It provides the backend API.

### 🟢 Health

```text
GET /health
```

Checks whether the application and Redis are available.

---

### 🟢 Start Session

```text
POST /api/session/start
```

Creates a unique session.

```text
START
  ↓
UUID
  ↓
SESSION CREATED
  ↓
ACTIVE
```

---

### 🟢 Send Frame

```text
POST /api/frame
```

The candidate browser sends camera frames here.

```text
📷 Frame
   ↓
Base64
   ↓
FastAPI
   ↓
Validation
   ↓
Redis
```

---

### 🟢 Get Alerts

```text
GET /api/alerts/{session_id}
```

Retrieves alerts for a specific candidate session.

---

### 🟢 Get Sessions

```text
GET /api/sessions
```

Retrieves available examination sessions.

---

# 📋 `08` — THE CONTRACT

## `schemas.py`

This file defines the structure of information entering the system.

Think of it as a **contract**.

```text
Camera Event
      │
      ▼
┌─────────────────────┐
│    FrameEvent       │
├─────────────────────┤
│ session_id          │
│ frame_base64        │
│ timestamp           │
└─────────────────────┘
```

If data doesn't follow the expected structure, the API can reject it.

---

# 👁️ `09` — THE OBSERVER

## `services/vision_worker/`

### Codename:

# 👁️ **THE ALL-SEEING EYE**

This is where Computer Vision enters the story.

```text
             CAMERA
                │
                ▼
        ┌───────────────┐
        │     FRAME     │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │    OpenCV     │
        └───────┬───────┘
                │
          ┌─────┼─────┐
          ▼     ▼     ▼
         🙂     👥     ❌
       NORMAL  ALERT  ERROR
```

---

# 🔬 `10` — DETECTION ENGINE

## `detector.py`

This file contains the Computer Vision detection logic.

### 👤 Single Face

```text
        ┌───────────┐
        │     🙂    │
        └───────────┘

           ↓

      NORMAL SIGNAL
```

---

### 🚫 No Face

```text
        ┌───────────┐
        │           │
        │     ?     │
        │           │
        └───────────┘

           ↓

       ⚠️ NO_FACE
```

---

### 👥 Multiple Faces

```text
        ┌───────────┐
        │   🙂  🙂  │
        └───────────┘

             ↓

     ⚠️ MULTIPLE_FACES
```

---

### 👀 Looking Away

```text
        ┌────────────┐
        │   🙂  →    │
        └────────────┘

              ↓

       ⚠️ LOOKING_AWAY
```

---

### 📷 Camera Error

```text
        📷
        │
        X
        │
        ▼
   CAMERA_ERROR
```

---

# ⚙️ `11` — THE WORKER

## `worker.py`

The worker continuously waits for new frames.

```text
WAIT
 │
 ▼
NEW FRAME?
 │
 ├── NO ──→ WAIT
 │
 └── YES
       │
       ▼
     DECODE
       │
       ▼
     ANALYZE
       │
       ▼
    DETECT EVENT
       │
       ▼
    SEND EVENT
       │
       ▼
      WAIT
```

This allows the heavy computer vision processing to remain separate from the API.

---

# 🔴 `12` — THE MESSENGER

## Redis Streams

Redis acts like the communication network between the characters.

```text
🚪 Gateway
    │
    │ "New Frame!"
    ▼
🔴 REDIS
    │
    │ "Here you go!"
    ▼
👁️ Vision Worker
```

This separation means the Gateway doesn't need to perform expensive computer vision processing itself.

---

# ⚖️ `13` — THE JUDGE

## `services/scoring_engine/`

The scoring engine processes detection events.

```text
             EVENT
               │
               ▼
        ┌──────────────┐
        │ SCORE ENGINE │
        └──────┬───────┘
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
    🟢 LOW   🟡 MED   🔴 HIGH
```

Different events can have different weights.

The result is **risk information**, not a final cheating decision.

---

# 🌐 `14` — THE TWO WORLDS

The project contains two separate interfaces.

```text
                 🌐 WEB
                   │
          ┌────────┴────────┐
          ▼                 ▼
     🧑‍🎓 CANDIDATE      🧑‍💼 PROCTOR
```

---

# 🧑‍🎓 `15` — CANDIDATE WORLD

Located inside:

```text
web/candidate/
```

### Files

```text
index.html
app.js
style.css
```

### Responsibilities

```text
🎥 Camera access
🧑‍🎓 Examination interface
📡 Frame transmission
🖥️ User interface
```

The candidate interface communicates with the Gateway.

---

# 🧑‍💼 `16` — PROCTOR WORLD

Located inside:

```text
web/proctor/
```

### Files

```text
index.html
app.js
style.css
```

This is the monitoring side of the system.

It can display:

```text
┌─────────────────────────────────────┐
│       🧑‍💼 PROCTOR DASHBOARD        │
├─────────────────────────────────────┤
│                                     │
│  SESSION       STATUS       ALERTS  │
│                                     │
│  #A102         🟢 ACTIVE      0     │
│  #A103         🟡 REVIEW      2     │
│  #A104         🔴 ALERT       5     │
│                                     │
└─────────────────────────────────────┘
```

---

# 🐳 `17` — THE MACHINE

## Docker

Docker gives every service its own environment.

```text
             🐳 DOCKER
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
   🚪 API      👁️ AI      ⚖️ SCORE
  Container   Container   Container
```

This makes the application easier to reproduce and deploy.

---

# 🚀 `18` — SUMMON THE SYSTEM

## Start with Docker

First create the environment file.

```bash
copy .env.example .env
```

Then:

```bash
docker compose up --build
```

The system will build and start its services.

---

# 🌐 `19` — ENTER THE WORLD

### 🧑‍🎓 Candidate Portal

```text
http://localhost:8000
```

### 🧑‍💼 Proctor Portal

```text
http://localhost:8000/proctor
```

### ❤️ System Health

```text
http://localhost:8000/health
```

---

# 🔥 `20` — ONE FRAME'S JOURNEY

Let's follow a single frame.

```text
                    📷
                    │
                    ▼
              CAMERA FRAME
                    │
                    ▼
              🧑‍🎓 BROWSER
                    │
                    ▼
              🚪 GATEWAY
                    │
                    ▼
              🔴 REDIS
                    │
                    ▼
             👁️ VISION AI
                    │
                    ▼
              🔍 ANALYSIS
                    │
             ┌──────┼──────┐
             ▼      ▼      ▼
            🙂     👥     ❌
             │      │      │
             └──────┼──────┘
                    ▼
              ⚠️ EVENT
                    │
                    ▼
              ⚖️ SCORING
                    │
                    ▼
               🔴 REDIS
                    │
                    ▼
             🧑‍💼 PROCTOR
```

---

# 🧠 `21` — WHY THIS ARCHITECTURE?

A simple project could do everything inside one Python file.

But that's not what this project is trying to demonstrate.

Instead:

```text
        ❌ ONE GIANT APPLICATION

                 VS

        ✅ SEPARATED SERVICES
```

Each component has its own responsibility.

```text
Gateway
   ↓
Handles communication

Vision Worker
   ↓
Handles AI/CV

Scoring Engine
   ↓
Handles scoring

Redis
   ↓
Handles communication/state

Frontend
   ↓
Handles user interaction
```

This makes the system easier to:

* Maintain
* Test
* Scale
* Debug
* Deploy
* Extend

---

# 🎮 `22` — TECHNOLOGY ARSENAL

```text
╔══════════════════════════════════════╗
║          ⚔️ TECHNOLOGY ARSENAL       ║
╠══════════════════════════════════════╣
║                                      ║
║ 🐍 Python       → Core Language      ║
║ ⚡ FastAPI      → Backend API        ║
║ 👁️ OpenCV      → Computer Vision    ║
║ 🔴 Redis       → Event Streaming     ║
║ 🌐 HTML        → Interface           ║
║ 🎨 CSS         → Design              ║
║ ⚙️ JavaScript  → Browser Logic       ║
║ 🐳 Docker      → Containers          ║
║ 🔧 Compose      → Service Management ║
║                                      ║
╚══════════════════════════════════════╝
```

---

# 🛡️ `23` — DEFENSE SYSTEM

A real-world proctoring platform must protect candidate information.

Before production deployment, the system should include:

```text
🔐 Authentication
        +
👮 Authorization
        +
🔒 HTTPS
        +
🗄️ Secure Data Storage
        +
🔑 Encryption
        +
📊 Monitoring
        +
🚦 Rate Limiting
```

Privacy and consent should be considered before collecting candidate camera data.

---

# ⚠️ `24` — THE AI IS NOT PERFECT

The system is an **AI-assisted detection system**.

It can make mistakes.

Possible problems include:

```text
🌑 Poor Lighting
📷 Low Camera Quality
👓 Glasses
🙈 Face Occlusion
📐 Camera Angle
🌐 Network Problems
👀 False Positives
❌ False Negatives
```

Therefore:

```text
        AI DETECTION
             │
             ▼
        ⚠️ SIGNAL
             │
             ▼
       👨‍💼 HUMAN REVIEW
             │
             ▼
        FINAL DECISION
```

### 🚫 Never:

```text
AI says CHEATING
       ↓
Automatically punish candidate
```

### ✅ Instead:

```text
AI detects unusual event
       ↓
Alert generated
       ↓
Human reviews
       ↓
Human decides
```

---

# 🌠 `25` — FUTURE EVOLUTION

The system can evolve into a much more advanced platform.

```text
                    🚀 FUTURE
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
  📱 Phone          🎙️ Audio         👤 Face
  Detection         Analysis        Tracking
       │               │               │
       └───────────────┼───────────────┘
                       ▼
                 🧠 ADVANCED AI
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
          📊 Data    📈 Risk    📝 Reports
          Analytics  Analysis   Generation
```

Possible future features:

* 📱 Mobile-phone detection
* 🎙️ Audio anomaly detection
* 👤 Advanced face tracking
* 👀 Improved gaze estimation
* 🧠 Better behavioral analysis
* 📊 Examination analytics
* 📈 Candidate risk timeline
* 📝 Automated reports
* 🔐 Role-based authentication
* ☁️ Cloud deployment
* 📦 Horizontal worker scaling

---

# ⚡ `26` — THE FINAL FLOW

```text
                         🌌
                    AI PROCTORING
                         │
                         ▼
                    🧑‍🎓 EXAM
                         │
                         ▼
                       📷
                      CAMERA
                         │
                         ▼
                     🚪 API
                         │
                         ▼
                    🔴 REDIS
                         │
                         ▼
                    👁️ AI/CV
                         │
                         ▼
                    ⚠️ EVENTS
                         │
                         ▼
                    ⚖️ SCORE
                         │
                         ▼
                    🧑‍💼 PROCTOR
                         │
                         ▼
                    👁️ HUMAN
                     REVIEW
                         │
                         ▼
                    🎯 DECISION
```

---

# 🏆 `27` — PROJECT HIGHLIGHTS

```text
╭──────────────────────────────────────╮
│                                      │
│       🤖 AI PROCTORING SYSTEM        │
│                                      │
│  ✓ Real-Time Frame Processing        │
│  ✓ Computer Vision Detection         │
│  ✓ Multiple Face Detection           │
│  ✓ No Face Detection                 │
│  ✓ Looking-Away Detection            │
│  ✓ Camera Error Detection            │
│  ✓ Event-Based Architecture          │
│  ✓ Redis Streams                     │
│  ✓ Separate AI Worker                │
│  ✓ Scoring Engine                    │
│  ✓ Candidate Interface               │
│  ✓ Proctor Dashboard                 │
│  ✓ Docker Architecture               │
│                                      │
╰──────────────────────────────────────╯
```

---

# 🎌 `28` — THE PHILOSOPHY

> ### **"The AI watches the screen.**
>
> ### **The system understands the signal.**
>
> ### **The human makes the decision."**

---

<div align="center">

# ⚡ AI PROCTORING SYSTEM

### `WATCH • ANALYZE • DETECT • ALERT`

```text
[ SYSTEM ONLINE ]

     👁️
     │
     ▼
  OBSERVING...

     🧠
     │
     ▼
  ANALYZING...

     ⚠️
     │
     ▼
  DETECTING...

     🧑‍💼
     │
     ▼
  HUMAN REVIEW

[ MISSION COMPLETE ]
```

### 🤖 Built with Python • FastAPI • OpenCV • Redis • Docker

</div>
