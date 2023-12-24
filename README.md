# Attractors take 3


Hey so a long time ago i found this https://examples.holoviz.org/attractors/attractors.html project and thought it looked really cool so i played around with it and wanted to turn it into a rest api.

It going to make me pretty pictures and server as a good test service for other things.


going to learn to use the .devcontainers

so im now in a clean 3.11 dev container :) I have a bash terminal

Cool so i updated my pre-commit hooks as well

Im running without a vevn bc im already in a clean room

# Redis
Idea to add some sort of caching for the attractors so if i want to recolor it i can pull the inital conditions from a chache

```bash
docker pull redis
# -p and --name must come before -d
docker run -p 6379 --name my-redis -d redis
docker exec -it my-redis redis-cli

set mykey "hello redis"
get mykey
```

```bash
pip install redis
pip install aioredis
```




# Issues
- Termial auto complete
- Can't build or run Dockerfile in the container.
possibly I could pass the local machines docker into the container
```bash
ls -la /var/run/docker.sock
docker run -v /var/run/docker.sock:/var/run/docker.sock -it your-dev-container-image
```

Maybe brew
