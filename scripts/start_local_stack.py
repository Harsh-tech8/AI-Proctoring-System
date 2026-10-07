import asyncio
import importlib
import os
import sys
import threading
import time
from pathlib import Path

import fakeredis.aioredis
import redis.asyncio
import uvicorn

ROOT = Path(__file__).resolve().parents[1]
os.environ["REDIS_URL"] = "fakeredis://localhost/0"
os.environ["EVENT_STREAM"] = "proctor:frames"
os.environ["ALERT_STREAM"] = "proctor:alerts"
os.environ["WEB_ROOT"] = str(ROOT / "web")

shared_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
orig_from_url = redis.asyncio.Redis.from_url


def fake_from_url(url, *args, **kwargs):
    if str(url).startswith("fakeredis://"):
        return shared_redis
    return orig_from_url(url, *args, **kwargs)


redis.asyncio.Redis.from_url = staticmethod(fake_from_url)


def import_service(service_dir: Path, module_name: str):
    for cached in list(sys.modules):
        if cached == "app" or cached.startswith("app."):
            del sys.modules[cached]
    sys.path.insert(0, str(service_dir))
    return importlib.import_module(module_name)


gateway_module = import_service(ROOT / "services" / "gateway", "app.main")
vision_module = import_service(ROOT / "services" / "vision_worker", "app.worker")
scoring_module = import_service(ROOT / "services" / "scoring_engine", "app.worker")


def run_gateway():
    uvicorn.run(gateway_module.app, host="0.0.0.0", port=8000, log_level="warning")


async def run_workers():
    await asyncio.gather(vision_module.main(), scoring_module.main())


if __name__ == "__main__":
    gateway_thread = threading.Thread(target=run_gateway, daemon=True)
    gateway_thread.start()
    time.sleep(1)
    try:
        asyncio.run(run_workers())
    except KeyboardInterrupt:
        pass
