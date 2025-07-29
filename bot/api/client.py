import aiohttp
from aiohttp import ClientResponse, ClientSession
from models.activity_level import ActivityLevel
from models.user import User


API_URL = 'http://localhost:8000'

# TODO: one connection per application
async def check_status(response: ClientResponse):
    if response.status != 200:
        text = await response.text()
        print("Status code:", response.status)
        print("Details:", text)
        response.raise_for_status()

async def create_user(user: User):
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.post(f"{API_URL}/user/create", json=user.model_dump()) as response:
            await check_status(response)

async def get_user(user_id: int) -> User:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"{API_URL}/user/get/{user_id}") as response:
            await check_status(response)

            user_data = await response.json()
            user = User(**user_data)
            return user

async def update_user(user: User):
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.patch(f"{API_URL}/user/update/{user.id}", json=user.model_dump()) as response:
            await check_status(response)

async def get_activity_level(level: int):
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"{API_URL}/level/get/{level}") as response:
            await check_status(response)

            data = await response.json()
            activity_level = ActivityLevel(**data)
            return activity_level

async def get_activity_levels() -> list[int]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"{API_URL}/level/all") as response:
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()
            
            data = await response.json()
            levels = sorted([level['level'] for level in data])
            return levels

async def get_activity_levels_descriptions():
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"{API_URL}/level/all") as response:
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()
            
            data = await response.json()
            descriptions_by_level = {}
            for level in data:
                descriptions_by_level[level['level']] = level['description']
            return descriptions_by_level

async def get_user_training_plan(user_id: int) -> str | None:
    """Get user's training plan from API's database."""
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"{API_URL}/plan/get/user/{user_id}") as response:
            if response.status == 404:
                return None
            await check_status(response)
            
            data = await response.json()
            plan = data['plan_description']
            return plan