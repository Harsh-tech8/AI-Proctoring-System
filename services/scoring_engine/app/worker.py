import asyncio
import os
from redis.asyncio import Redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
ALERT_STREAM = os.getenv("ALERT_STREAM", "proctor:alerts")
GROUP = "scoring-workers"
CONSUMER = os.getenv("HOSTNAME", "scoring-engine")

WEIGHTS = {
    "NORMAL": 0,
    "NO_FACE": 3,
    "LOOKING_AWAY": 2,
    "MULTIPLE_FACES": 5,
    "CAMERA_ERROR": 3,
    "EYE_CLOSED": 2,
    "TAB_SWITCH": 4,
    "PROCESSING_ERROR": 2,
}

async def ensure_group(redis):
    try:
        await redis.xgroup_create(ALERT_STREAM, GROUP, id="0", mkstream=True)
    except Exception:
        pass

async def main():
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
    await ensure_group(redis)
    print("Scoring engine started.")

    while True:
        batches = await redis.xreadgroup(
            GROUP, CONSUMER, {ALERT_STREAM: ">"}, count=10, block=5000
        )
        if not batches:
            continue

        for _, messages in batches:
            for message_id, data in messages:
                session_id = data["session_id"]
                signal = data.get("signal", "NORMAL")
                severity = int(data.get("severity", WEIGHTS.get(signal, 1)))
                confidence = float(data.get("confidence", "0"))
                points = round(severity * confidence, 2)

                key = f"session:{session_id}"
                await redis.hincrbyfloat(key, "score", points)

                score = float(await redis.hget(key, "score") or 0)
                status = "REVIEW_REQUIRED" if score >= 10 else "ACTIVE"
                await redis.hset(key, mapping={
                    "status": status,
                    "last_signal": signal,
                    "last_message": data.get("message", ""),
                })

                await redis.xack(ALERT_STREAM, GROUP, message_id)

if __name__ == "__main__":
    asyncio.run(main())
