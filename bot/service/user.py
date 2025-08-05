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
    except:
        # there is a user with this ID, update data
        await api_client.update_user(user)
