import asyncio

from aiocache import caches
from another import do_i_get_the_same

# You can use either classes or strings for referencing classes
caches.set_config({
    'default': {
        'cache': "aiocache.SimpleMemoryCache",
        'serializer': {
            'class': "aiocache.serializers.StringSerializer"
        }
    },
    'redis_alt': {
        'cache': "aiocache.RedisCache",
        'endpoint': "my_redis_container",
        'port': 6379,
        'timeout': 1,
        'serializer': {
            'class': "aiocache.serializers.PickleSerializer"
        },
        'plugins': [
            {'class': "aiocache.plugins.HitMissRatioPlugin"},
            {'class': "aiocache.plugins.TimingPlugin"}
        ]
    }
})


async def default_cache():
    cache = caches.get('default')   # This always returns the SAME instance
    print(await do_i_get_the_same())
    await cache.set("key", "value")
    print(await do_i_get_the_same())
    print(await cache.get("key"))


async def alt_cache():
    cache = caches.create('redis_alt')   # This creates a NEW instance on every call
    await cache.set("key", "value")
    assert await cache.get("key") == "value"


async def test_alias():
    await default_cache()
    await alt_cache()

    await caches.get("redis_alt").delete("key")


if __name__ == "__main__":
    asyncio.run(test_alias())
