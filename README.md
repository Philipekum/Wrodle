# Wrodle
My custom [Wordle](https://www.nytimes.com/games/wordle/)-clone, created as my hobbie. Tried to make it clean, modern and proper.
Wrodle is not a typo (!!!), that's a slightly off name for my clone.
The project is in early stages of developing, future plans are written in [ROADMAP.md](docs/ROADMAP.md)

# Technologies
I am using modern sync stack of a RESTful API. Tried to not overengineer such a simple app. 

## Backend
Fastapi + redis (partially as db). I don't want to use Postgres for the 100th time. Long term records will be stored in DuckDB, simply because I wanted to try using it.

## Frontend
I want to make a SPA-client or some simple htmx-logic, not sure right now.
I am not a frontender myself, so it wouldnt be the strongest part of project

## Telegram
I will use aiogram3 to create a simple bot to play Wrodle there. Also it is a test for integration compatibility of API.

## Reverse Proxy
NGINX, as always.

## Infrastructure
Basic docker-compose config is enough for this project, don't want to use k8s just for flex. A base sync uvicorn+nginx app.
However I will flex CI/CD just to test it on a small scale of this project. GHActions are already integrated. Also I use pre-commit (with ruff and mypy) and commitizen.

# Current project structure
API is not versioned (single-developer project). Breaking changes are possible - ping me if you build on top of it.

.
├── app
│   ├── api
│   │   ├── api_router.py
│   │   ├── routes
│   │   │   ├── game.py
│   │   │   └── utils.py
│   │   └── schemas.py
│   ├── config.py
│   ├── deps.py
│   ├── Dockerfile
│   ├── main.py
│   └── services
│       ├── game_logic.py
│       └── types.py
├── redis
│   ├── Dockerfile
│   └── redis.conf
├── tests
│   ├── conftest.py
│   └── test_utils
│       └── test_health_check.py
├── docs
│   └── ROADMAP.md
├── docker-compose.yaml
├── pyproject.toml
├── LICENSE
├── README.md
└── uv.lock

# Get Started
This is not even a realese, so don't start!
