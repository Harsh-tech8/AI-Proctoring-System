import base64
import json
import os
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from .schemas import AlertEvent, FrameEvent

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
EVENT_STREAM = os.getenv("EVENT_STREAM", "proctor:frames")
ALERT_STREAM = os.getenv("ALERT_STREAM", "proctor:alerts")

app = FastAPI(title="AI Proctoring Gateway", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = Redis.from_url(REDIS_URL, decode_responses=True)
WEB_ROOT = Path(os.getenv("WEB_ROOT", "/app/web"))
if not WEB_ROOT.exists():
    WEB_ROOT = Path(__file__).resolve().parents[3] / "web"

@app.get("/health")
async def health():
    try:
        await redis.ping()
        return {"status": "ok", "redis": "ok"}
    except Exception as exc:
        return {"status": "degraded", "redis": str(exc)}

@app.post("/api/session/start")
async def start_session():
    import uuid
    session_id = str(uuid.uuid4())
    await redis.hset(f"session:{session_id}", mapping={
        "score": 0,
        "status": "ACTIVE",
        "last_seen": time.time(),
    })
    await redis.expire(f"session:{session_id}", 3600)
    return {"session_id": session_id, "status": "ACTIVE"}

@app.post("/api/frame")
async def submit_frame(event: FrameEvent):
    try:
        base64.b64decode(event.frame_base64.split(",", 1)[-1])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 frame")

    session_key = f"session:{event.session_id}"
    if await redis.exists(session_key):
        session_data = await redis.hgetall(session_key)
        updates = {"last_seen": time.time()}
        if session_data.get("status") == "INACTIVE":
            updates["status"] = "ACTIVE"
        await redis.hset(session_key, mapping=updates)

    await redis.xadd(EVENT_STREAM, {
        "session_id": event.session_id,
        "frame_base64": event.frame_base64,
        "timestamp": str(event.timestamp),
    }, maxlen=10000, approximate=True)

    return {"accepted": True}

@app.post("/api/event")
async def submit_event(event: AlertEvent):
    await redis.xadd(ALERT_STREAM, {
        "session_id": event.session_id,
        "signal": event.signal,
        "severity": str(event.severity),
        "confidence": str(event.confidence),
        "message": event.message,
        "timestamp": str(event.timestamp or 0),
    }, maxlen=10000, approximate=True)
    return {"accepted": True}

@app.get("/api/alerts/{session_id}")
async def alerts(session_id: str):
    items = []
    messages = await redis.xrevrange(ALERT_STREAM, count=10000)
    for _, data in messages:
        if data.get("session_id") == session_id:
            items.append(data)
            if len(items) >= 200:
                break
    return {"session_id": session_id, "alerts": items}

@app.get("/api/sessions")
async def sessions():
    keys = []
    async for key in redis.scan_iter(match="session:*"):
        keys.append(key)
    result = []
    now = time.time()
    for key in keys:
        data = await redis.hgetall(key)
        try:
            last_seen = float(data.get("last_seen", 0))
        except (TypeError, ValueError):
            last_seen = 0
        status = data.get("status", "ACTIVE")
        if status != "REVIEW_REQUIRED" and (not last_seen or now - last_seen > 8):
            status = "INACTIVE"
            await redis.hset(key, "status", status)
        result.append({"session_id": key.split(":", 1)[1], **data})
        result[-1]["status"] = status
        result[-1]["last_seen"] = last_seen
    return {"sessions": result}

@app.get("/")
async def candidate():
    return FileResponse(WEB_ROOT / "candidate" / "index.html")

@app.get("/candidate/{filename}")
async def candidate_assets(filename: str):
    return FileResponse(WEB_ROOT / "candidate" / filename)

@app.get("/proctor")
async def proctor():
    return FileResponse(WEB_ROOT / "proctor" / "index.html")

@app.get("/proctor/{filename}")
async def proctor_assets(filename: str):
    return FileResponse(WEB_ROOT / "proctor" / filename)
