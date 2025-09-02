"""Client for the API."""
from typing import Any
import logging
from aiohttp import ClientResponse, ClientSession
from models.activity_level import ActivityLevel
from models.user import User
from config import config


logger = logging.getLogger(__name__)

async def check_response_status(response: ClientResponse):
    """Checks request's response status.

    Use to confirm a successful request.

    Args:
        response (`ClientResponse`): aiohttp request to the API
    """
    status = response.status
    text = await response.text()
    if status != 200:
        logger.error("API request error [STATUS %i]: %s", status, text)
        response.raise_for_status()
    else:
        logger.info("API request [STATUS %i]: %s", status, text)


class APIClient:
    """API client class. Allows to make different requests to the API."""

    def __init__(self):
        """
        Create client and session.

        Use only once on bot's **start up**.
        """
        self.session = ClientSession(config.API_BASE_URL)

    async def close_session(self):
        """Close API aiohttp session.

        Use on bot **shutdown**.
        """
        await self.session.close()

    async def get_user_request_response(self, user_id: int, request: str):
        """Get AI response on user's request using the API.

        Args:
            user_id (`int`): user Telegram ID
            request (`str`): text message from user to AI
        """
        request_body = {
            "user_id": user_id,
            "content": request
        }
        async with self.session.post("/user/chat", json=request_body) as response:
            await check_response_status(response)
            return await response.text()

    async def create_user(self, user: User):
        """Create user entry in API's database.

        Can't create user with the ID that already exists.

        Args:
            user (`User`): user data for creation
        """
        async with self.session.post("/user/create",
                                     json=user.model_dump()) as response:
            await check_response_status(response)

    async def get_user(self, user_id: int) -> User:
        """Get user entry from API by their ID.

        Args:
            user_id (`int`): user Telegram ID
        """
        async with self.session.get(f"/user/get/{user_id}") as response:
            await check_response_status(response)
            user_data = await response.json()
            user = User(**user_data)
            return user

    async def update_user_field(self,
                                user_id: int,
                                field_name: str,
                                value: Any):
        """Update one exact field of the user.

        Uses User model.

        Can update only existing user.

        Args:
            user_id (`int`): user Telegram ID
            field_name (`str`): User model field name
            value (`Any`): new value for the field
        """
        request_body = {field_name: value}
        async with self.session.patch(f"/user/update/{user_id}",
                                      json=request_body) as response:
            await check_response_status(response)

    async def update_user(self, user: User):
        """Update data of the user.

        Can update only existing user.

        Args:
            user (`User`): new data for the user
        """
        async with self.session.patch(f"/user/update/{user.id}",
                                      json=user.model_dump()) as response:
            await check_response_status(response)

    async def get_activity_level(self, level: int) -> ActivityLevel:
        """Get activity level data by 'level' field.

        Args:
            level (`int`): activity level number
        """
        async with self.session.get(f"/level/get/{level}") as response:
            await check_response_status(response)
            data = await response.json()
            activity_level = ActivityLevel(**data)
            return activity_level

    async def get_activity_levels(self) -> list[ActivityLevel]:
        """Get all possible activity levels from API."""
        async with self.session.get("/level/all") as response:
            await check_response_status(response)
            data = await response.json()
            # return all levels sorted by 'level' field
            levels = sorted([ActivityLevel(**level) for level in data],
                            key=lambda x: x.level)
            return levels

    async def create_user_training_plan(self, user_id: int, user_request: str):
        """Create a training plan for user using API.

        The API creates training plans with AI.
        """
        request_body = {
            'user_id': user_id,
            'content': user_request
        }
        async with self.session.post("/plan/generate",
                                     json=request_body) as response:
            await check_response_status(response)

    async def get_user_training_plan(self, user_id: int) -> str:
        """Get user's training plan from API's database.

        Args:
            user_id (`int`): user Telegram ID
        """
        async with self.session.get(f"/plan/get/user/{user_id}") as response:
            await check_response_status(response)
            data = await response.json()
            plan = data['plan_description']
            return plan
