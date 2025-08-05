from api.client import APIClient


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