import asyncio
import os

import fakeredis.aioredis
import redis.asyncio

os.environ["REDIS_URL"] = "fakeredis://localhost/0"
os.environ["EVENT_STREAM"] = "proctor:frames"
os.environ["ALERT_STREAM"] = "proctor:alerts"

shared = fakeredis.aioredis.FakeRedis(decode_responses=True)
orig_from_url = redis.asyncio.Redis.from_url

def fake_from_url(url, *args, **kwargs):
    if str(url).startswith("fakeredis://"):
        return shared
    return orig_from_url(url, *args, **kwargs)

redis.asyncio.Redis.from_url = staticmethod(fake_from_url)

async def run_test():
    print('shared type', type(shared))
    await shared.xadd('proctor:alerts', {'session_id': 'abc', 'signal': 'NO_FACE', 'severity': '3', 'confidence': '1.0', 'message': 'x'}, maxlen=10000, approximate=True)
    print('after add', await shared.xrange('proctor:alerts'))
    try:
        await shared.xgroup_create('proctor:alerts', 'scoring-workers', id='0', mkstream=True)
        print('group created')
    except Exception as exc:
        print('group create failed', type(exc), exc)
    print('group members', await shared.xinfo_groups('proctor:alerts'))
    result = await shared.xreadgroup('scoring-workers', 'consumer', {'proctor:alerts': '>'}, count=10, block=100)
    print('readgroup result', result)

asyncio.run(run_test())
