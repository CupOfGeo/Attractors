import asyncio

import aioredis


async def get_redis_pool() -> aioredis.Redis:
    """Get a redis connection pool."""
    return await aioredis.create_redis_pool("redis://127.0.0.1:6379", encoding="utf-8")


async def test_redis_connection():
    pool = await get_redis_pool()
    await pool.set('test_key', 'test_value')
    value = await pool.get('test_key')
    if value == 'test_value':
        print("Redis connection is working fine.")
    else:
        print("Failed to connect to Redis.")

# Run the test
asyncio.run(test_redis_connection())
