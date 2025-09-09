# AI-coach Telegram Bot with API

## About
This is a Telegram Bot that uses specially developed API to work
as a trainer for a Telegram user. It can be helpful for those who train or want to stay healthy and at the same time
don't want to spend time searching for answers.

You can create a profile with your parameters and
the bot will use them to:
  1) create training plans
  2) make advices
  3) motivate you

## Goals
I wanted to practice my developer skills and try out new frameworks and libraries.

I was trying to use best practices, making future upgrades easier.

Also it was important to create an app that I would use, something useful.

## Structure
***Bot***: the interface for users, doesn't store any data, delegates this to the API. Makes API requests.

***API***: CRUD operations with data, makes AI API requests.

***LLM API***: AI API for training plan/user request response generation.
****

## Tools used
- **Aiogram** - an asynchrounous framework for Telegram Bot API (to develop the bot)
- **FastAPI** - a web framework for building APIs (to develop the API)
- **Redis** - a NoSQL database (to use FSM in the bot)
- **SQLAlchemy** - an ORM and SQL toolkit (to make work with database easier)
- **Alembic** - a database migration tool (to create database from SQLAlchemy models) 
- **PostgreSQL** - a SQL database (a stable and popular tool)
  - **Asyncpg** - a database interface library for async. work (to process multiple requests)
- **Pydantic** - a data validation library (to store and validate data)
- **Aiohttp** - an asynchronous HTTP client (to make async. requests)
- **Uvicorn** - an ASGI web server (to launch the API)
- **Docker** - a deployment tool (to launch Redis/PostgreSQL)
- **OpenAI** - an SDK for OpenAI API (to get AI responses)

## Quick start
***---STILL UNDER CONSTRUCTION---***

***No docker contrainers yet***

It is recommended to use venv for installing all of the dependencies.

1) Clone the repository
2) Install dependencies in `requirements.txt`:
```bash
pip install -r requirements.txt
```
3) Create `.env` file based on `.env_example`
4) Go to project's directory and launch the bot and api (note that they are launched as packages):

Launch the _api_
```bash
python -m api.main
```
Launch the _bot_
```bash
python -m bot.main
```

## Bot guide
#### 1. Start the bot
In Telegram use a link to go to the chat with the bot and press ***start***.

Fill in your data (age, weight, etc.) and you should be ready to use the bot.
#### 2. Choose a menu action
You can use the bot with special bot commands (`/start', for example), they will be displayed in the menu.

##### BOT COMMANDS
|Command   	|Description   	|
|---	|---	|
|`/help`|Get info about bot usage and list of commands|
|`/start`|Create your profile from scratch|
|`/profile`|Inspect your profile and edit its fields|
|`/generate_plan`|Generate a training plan|
|`/my_plan`|Inspect your current training plan|

If you want to simply communicate with the bot, just send him a message (for example, "Is it okay to workout everyday?").

## API guide
This API is designed to store, write and access data

You can get all information you need using FastAPI documentation for the API
Access this documentation via links (if you use on local machine):
- `localhost:your_port/docs`
- `localhost:your_port/redoc`

#### Base URL scheme
There are URL groups for all models in the API:
- `/user`
- `/training plan`
- `/activity level`

For each group there are CRUD operations paths
and some unique specific ones:
- `/create`
- `/delete`
- `/generate` - for training plans only

They may require some path parameters

#### Some useful paths
|URL   	|Description   	|
|---	|---	|
|`/user/create`|Create a new user|
|`/user/get/{user_id}`|Get the user with ID=user_id|
|`/plan/generate`|Generate a training plan for a user using AI|
