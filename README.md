# Attractors take 3
Hey so a long time ago i found this https://examples.holoviz.org/attractors/attractors.html project and thought it looked really cool so i played around with it and wanted to turn it into a rest api.

It was a super cool demo learned about jit and datashaders

It going to make me pretty pictures and the server will be a good test service for other things.

going to learn to use the .devcontainers

so im now in a clean 3.11 dev container :) I have a bash terminal

Cool so i updated my pre-commit hooks as well

Im running without a vevn bc im already in a clean room

# Redis
Idea to add some sort of caching for the attractors so if i want to recolor it i can pull the inital conditions from a chache

```bash
docker pull redis
# -p and --name must come before -d
docker run -p 6379:6379 --name my-redis -d redis
docker exec -it my-redis redis-cli

set mykey "hello redis"
get mykey
```

```bash
pip install redis
pip install aioredis
```

Redis is cool but its overkill I can just use `from cachetools import TTLCache`
No thats not async enough im going to use `from aiocache import caches`

Im now seeing in jit that it can do caching. But that wouldnt be helpful as my function does one iteration at a time and i just cache the resulting 10000000 iterations with the intial conditions. I also compres it with gzip so which is nice too.


# Issues
- Termial auto complete
- Can't build or run Dockerfile in the container.
possibly I could pass the local machines docker into the container
```bash
ls -la /var/run/docker.sock
docker run -v /var/run/docker.sock:/var/run/docker.sock -it your-dev-container-image
```

- I'm running redis on port 6379 but i cant connect to it bc im in a container
    - ok so i had to do this
    ```bash
    docker network create my_network
    # re run a new redis instance with the --network
    docker run --name my_redis_container --network my_network -p 6379:6379 -d redis
    # i had to also add my_network to the build args of this in devcontainer.json
    ```

- Brew 🍺 would be nice
