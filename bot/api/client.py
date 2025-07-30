from aiohttp import ClientResponse, ClientSession
from models.activity_level import ActivityLevel
from models.user import User


async def check_response_status(response: ClientResponse):
    if response.status != 200:
        text = await response.text()
        print("Status code:", response.status)
        print("Details:", text)
        response.raise_for_status()

class APIClient:
    _API_URL_BASE = 'http://localhost:8000'
    
    def __init__(self):
        """
        Create client and session.
        Use only once on bot's start up.
        """
        self.session = ClientSession(self._API_URL_BASE)
        
    async def close_session(self):
        """
        Close API aiohttp session.
        Use on bot shutdown.
        """
        await self.session.close()

    async def create_user(self, user: User):
        """
        Create user entry in API's database.
        Can't create user with ID that already exists.
        """
        async with self.session.post("/user/create", 
                                     json=user.model_dump()) as response:
            await check_response_status(response)

    async def get_user(self, user_id: int) -> User:
        """
        Get user entry from API by their ID.
        """
        async with self.session.get(f"/user/get/{user_id}") as response:
            await check_response_status(response)
            user_data = await response.json()
            user = User(**user_data)
            return user

    async def update_user_field(self, user_id: int, field_name: str, value):
        """
        Update data of the user.
        Can update only existing user.
        """
        async with self.session.patch(f"/user/update/{user_id}", 
                                      json={field_name: value}) as response:
            await check_response_status(response)

    async def get_activity_level(self, level: int):
        """
        Get activity level data by 'level' field.
        """
        async with self.session.get(f"/level/get/{level}") as response:
            await check_response_status(response)
            data = await response.json()
            activity_level = ActivityLevel(**data)
            return activity_level

    async def get_activity_levels(self) -> list[ActivityLevel]:
        """
        Get all possible activity levels from API.
        """
        async with self.session.get("/level/all") as response:
            await check_response_status(response)
            data = await response.json()
            # return all levels sorted by 'level' field
            levels = sorted([ActivityLevel(**level) for level in data], 
                            key=lambda x: x.level)
            return levels

    async def get_user_training_plan(self, user_id: int) -> str | None:
        """
        Get user's training plan from API's database.
        """
        async with self.session.get(f"/plan/get/user/{user_id}") as response:
            if response.status == 404:
                return None
            await check_response_status(response)
            data = await response.json()
            plan = data['plan_description']
            return plan
