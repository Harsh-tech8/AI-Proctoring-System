import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICE_ROOT = ROOT / "services" / "gateway"
os.chdir(SERVICE_ROOT)
sys.path.insert(0, str(SERVICE_ROOT))

import fakeredis.aioredis
import redis.asyncio
import uvicorn

os.environ["REDIS_URL"] = "fakeredis://localhost/0"
os.environ["EVENT_STREAM"] = "proctor:frames"
os.environ["ALERT_STREAM"] = "proctor:alerts"
os.environ["WEB_ROOT"] = str(ROOT / "web")

orig_from_url = redis.asyncio.Redis.from_url


def fake_from_url(url, *args, **kwargs):
    if str(url).startswith("fakeredis://"):
        return fakeredis.aioredis.FakeRedis(decode_responses=True)
    return orig_from_url(url, *args, **kwargs)


redis.asyncio.Redis.from_url = staticmethod(fake_from_url)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
