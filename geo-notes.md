# Redis
Idea to add some sort of caching for the attractors so if i want to recolor it i can pull the initial conditions from a cache

```bash
docker pull redis
# -p and --name must come before -d
docker run -p 6379:6379 --name my-redis -d redis
docker exec -it my-redis redis-cli

set my-key "hello redis"
get my-key
```

```bash
pip install redis
pip install aioredis
```

Redis is cool but its overkill I can just use `from cachetools import TTLCache`
No thats not async enough im going to use `from aiocache import caches`

Im now seeing in jit that it can do caching. But that wouldn't be helpful as my function does one iteration at a time and i just cache the resulting 10000000 iterations with the initial conditions. I also compress it with gzip so which is nice too.
