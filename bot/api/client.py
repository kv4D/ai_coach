import aiohttp
from aiohttp import ClientResponse, ClientSession
from models.activity_level import ActivityLevel
from models.user import User


async def check_status(response: ClientResponse):
    if response.status != 200:
        text = await response.text()
        print("Status code:", response.status)
        print("Details:", text)
        response.raise_for_status()

class APIClient:
    _API_URL_BASE = 'http://localhost:8000'
    
    def __init__(self):
        self.session = ClientSession(self._API_URL_BASE)
        
    async def close_session(self):
        """
        Close API aiohttp session.
        Use on_
        """
        await self.session.close()

    async def create_user(self, user: User):
        async with self.session.post("/user/create", json=user.model_dump()) as response:
            await check_status(response)

    async def get_user(self, user_id: int) -> User:
        async with self.session.get(f"/user/get/{user_id}") as response:
            await check_status(response)
            user_data = await response.json()
            user = User(**user_data)
            return user

    async def update_user(self, user: User):
        async with self.session.patch(f"/user/update/{user.id}", json=user.model_dump()) as response:
            await check_status(response)

    async def get_activity_level(self, level: int):
        async with self.session.get(f"/level/get/{level}") as response:
            await check_status(response)
            data = await response.json()
            activity_level = ActivityLevel(**data)
            return activity_level

    async def get_activity_levels(self) -> list[int]:
        async with self.session.get("/level/all") as response:
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()
            
            data = await response.json()
            levels = sorted([level['level'] for level in data])
            return levels

    async def get_activity_levels_descriptions(self):
        async with self.session.get("/level/all") as response:
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

    async def get_user_training_plan(self, user_id: int) -> str | None:
        """Get user's training plan from API's database."""
        async with self.session.get(f"/plan/get/user/{user_id}") as response:
            if response.status == 404:
                return None
            await check_status(response)
            data = await response.json()
            plan = data['plan_description']
            return plan