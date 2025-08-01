# AI-coach Telegram Bot with API

## About
This is a Telegram Bot that uses specially developed API to work
as a trainer for a Telegram user
You can create a profile with your parameters and
the bot will use them to:
  1) create training plans
  2) make advices
  3) motivate you

## Goals
I wanted to practice my developer skills and try out new frameworks and libraries.
I was trying to use best practices, making future upgrades easier.
Also it was important to create an app that I would use, something helpful.

## Structure
**Bot**: the interface for users, doesn't store any data, delegates this to the API. Makes API requests.
**Api**: CRUD operations with data, makes AI API requests.
  - **LLM**: AI API for training plan/user request response generation.
****

## Technologies used
- Aiogram - an asynchrounous framework for Telegram Bot API
- FastAPI - a web framework for building APIs
- Redis - a NoSQL database
- SQLAlchemy - an ORM and SQL toolkit
- Alembic - a database migration tool
- PostgreSQL - a SQL database
  - Asyncpg - a database interface library for async. work
- Pydantic - a data validation library
- Aiohttp - an asynchronous HTTP client
- Uvicorn - an ASGI web server
- Docker - a deployment tool
- OpenAI - an SDK for OpenAI API

## Quick start
It is recommended to use venv.

1) Clone the repository
2) Install dependencies in requirements.txt:
```bash
pip install -r requirements.txt
```
3) Create .env file based on .env_example
4) Go to project's directory and launch bot and api:

Launch _api_
```bash
python api/main.py
```
Launch _bot_
```bash
python bot/main.py
```

## Bot guide

## API guide
