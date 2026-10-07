import asyncio
import json
import os

from redis.asyncio import Redis

from .detector import analyze

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
EVENT_STREAM = os.getenv("EVENT_STREAM", "proctor:frames")
ALERT_STREAM = os.getenv("ALERT_STREAM", "proctor:alerts")
GROUP = "vision-workers"
CONSUMER = os.getenv("HOSTNAME", "vision-worker")

async def ensure_group(redis):
    try:
        await redis.xgroup_create(EVENT_STREAM, GROUP, id="0", mkstream=True)
    except Exception:
        pass

async def main():
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
    await ensure_group(redis)
    print("Vision worker started.")

    while True:
        batches = await redis.xreadgroup(
            GROUP, CONSUMER, {EVENT_STREAM: ">"}, count=1, block=5000
        )
        if not batches:
            continue

        for _, messages in batches:
            for message_id, data in messages:
                session_id = data["session_id"]
                try:
                    detections = analyze(data["frame_base64"])
                    for detection in detections:
                        payload = {
                            "session_id": session_id,
                            "signal": detection.signal,
                            "severity": detection.severity,
                            "confidence": detection.confidence,
                            "message": detection.message,
                            "timestamp": data.get("timestamp", ""),
                        }
                        await redis.xadd(ALERT_STREAM, payload, maxlen=10000, approximate=True)
                    await redis.xack(EVENT_STREAM, GROUP, message_id)
                except Exception as exc:
                    await redis.xadd(ALERT_STREAM, {
                        "session_id": session_id,
                        "signal": "PROCESSING_ERROR",
                        "severity": "2",
                        "confidence": "1.0",
                        "message": str(exc),
                    })
                    await redis.xack(EVENT_STREAM, GROUP, message_id)

if __name__ == "__main__":
    asyncio.run(main())
