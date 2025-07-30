from api.client import APIClient


async def get_activity_levels_description(api_client: APIClient):
    try:
        levels = await api_client.get_activity_levels()
        message_str = ""
        for level in levels:
            message_str += f"{level.get_formatted_string()}\n"
        return message_str
    except:
        raise