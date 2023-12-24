from aiocache import caches


async def do_i_get_the_same():
    cache = caches.get("default")
    return await cache.get("key")
