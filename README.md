# Space-X challenge

FastAPI offline challenge ([Challenge requirements](https://doc.clickup.com/459857/d/h/e12h-61863/14674106a2a38cc)).


### System Requirements

* [Docker](https://docs.docker.com/engine/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Clone repository
```shell
git pull https://github.com/Abrunacci/space_x_challenge.git
cd space_x_challenge
```

### Environment variables values
This two files should be already in the repository. If not, please create both with the following values.

`Docker/development/env/public`
```shell
TRELLO_API_BASE_URL=https://api.trello.com/1/
LOG_LEVEL=debug
API_HOST=0.0.0.0
ENVIRONMENT=develop
BOARD_NAME=SpaceXChallenge
```

`Docker/development/env/private`
```shell
TRELLO_API_KEY=faa8b65898f3f7d84483cfd4e73dd3c1
TRELLO_API_TOKEN=ATTAa9ce010f959f1f7870857be489ce327330e01fb190a094687ca02b9ca8ad8a4645F7AEE2
TRELLO_API_USER=abrunacci87userintegration1
```

If you weren't provided with the Trello API key and token, [you can create one for your boards](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/).
### Run application

```shell
docker compose build
docker compose up -d
```

### End application

```shell
docker compose down
```

### Run tests

```shell
docker compose up -d
docker compose exec api pytest . -v --cov-report  --cov
docker compose down
```

# API Test Coverage:

```shell
---------- coverage: platform linux, python 3.10.13-final-0 ----------
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
src/connectors/trello_connector.py      22      0   100%
src/exceptions/trello_connector.py       8      0   100%
src/exceptions/trello_service.py         4      0   100%
src/main.py                              9      0   100%
src/routers/trello.py                   10      0   100%
src/schemas/tasks.py                     8      0   100%
src/services/trello.py                  62      0   100%
--------------------------------------------------------
TOTAL                                  123      0   100%



```

# API Endpoints

### [GET] http://0.0.0.0:3000/docs

    Redirects to API documentation.

    curl 'http://0.0.0.0:3000/docs'

### [POST] http://0.0.0.0:3000/

    Creates a new task.

    {
        "type": "task type",
        "title": "task title" [optional], 
        "description": "task description" [optional],
        "category": "task category" [optional]
    }

    curl -X 'POST' 'http://localhost:3000/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"type": "bug", "description": "another day, another bug"}'

---

# Trello board:
https://trello.com/b/WS3irMZu/spacexchallenge