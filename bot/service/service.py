from api.client import APIClient
from models.user import User


# TODO: make exceptions certain
async def create_user(user: User, api_client: APIClient):
    """Create a user entry in API.

    If the user already exists, update data.

    Args:
        user (`User`): user data for creation
        api_client (`APIClient`): an API client to make requests
    """
    try:
        await api_client.create_user(user)
    except Exception as e:
        print(e)
        # there is a user with this ID, update data
        await api_client.update_user(user)

async def create_user_training_plan(user_id: int, user_request: str, api_client: APIClient):
    """Create a training plan for the user."""
    await api_client.create_user_training_plan(user_id, user_request)

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