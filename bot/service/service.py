from api.client import APIClient
from aiohttp import ClientResponseError
from models.user import User


async def create_user(user: User, api_client: APIClient):
    """Create a user entry in API.

    If the user already exists, update data.

    Args:
        user (`User`): user data for creation
        api_client (`APIClient`): an API client to make requests
    """
    try:
        await api_client.create_user(user)
    except ClientResponseError:
        # there is a user with this ID, update data
        await api_client.update_user(user)


async def get_activity_levels_description(api_client: APIClient) -> str:
    """Get activity levels descriptions.

    Provides string that contains:
    - all levels
    - all fields for every activity level

    Args:
        api_client (`APIClient`): an API client to make requests
    """
    try:
        levels = await api_client.get_activity_levels()
        message_str = ""
        for level in levels:
            message_str += f"{level.get_formatted_string()}\n"
        return message_str
    except:
        raise


async def is_user_exist(user_id: int, api_client: APIClient) -> bool:
    """Check if the user is present in the database.

    Args:
        user_id (`int`): user Telegram ID
        api_client (`APIClient`): an API client to make requests
    """
    try:
        await api_client.get_user(user_id)
        return True
    except ClientResponseError:
        # no user found
        return False
