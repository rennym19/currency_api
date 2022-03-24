# Currency Convert API

Currency Convert API was made so that you can easily convert any of the
available currencies!

## Running the project

The simplest and most straight-forward way to get this up and running is using [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).

Just run the following:

```sh
docker-compose up -d --build
```

## Api Docs

Exposed on `/docs`

## Intentionally left out

Since this is meant to be a small/quick task, some extra features and/or nice-to-have(s) have been left out, some of them being:

- Time-series data (API limitations)
- Unit testing (pytest)
- Key obfuscation (the API key is at plain sight)
- Use of `.env` for environment / config. variables
- Logging to a file ([loguru](https://github.com/Delgan/loguru) would work great w/ FastAPI)
