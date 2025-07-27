from webbrowser import get
from asyncio import run
import aiohttp


API_URL = 'http://localhost:8000'


async def create_user(user_data: dict):
    async with aiohttp.ClientSession() as session:
        # check for user
        async with session.get(f"{API_URL}/user/get/{user_data['id']}") as response:
            if response.status == 200:
                return await update_user(user_data)
        
        user_data['activity_level_id'] = await get_activity_level_id(user_data["activity_level"])
        async with session.post(f"{API_URL}/user/create", json=user_data) as response:
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()


async def get_user_data(user_id: int) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/user/get/{user_id}") as response:
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()
            else:
                user_data = await response.json()
                return render_user_data(user_data)


def render_user_data(user_data: dict) -> str:
    """Transform user data dictionary into a formatted string for display."""
    formatted_data = []
    
    # field names to show
    fields = {
        'username': '<strong>Имя пользователя</strong>',
        'age': '<strong>Возраст</strong>',
        'weight_kg': '<strong>Вес (кг)</strong>',
        'height_cm': '<strong>Рост (см)</strong>',
        'activity_level': '<strong>Уровень активности</strong>',
        'goal': '<strong>Цель тренировок</strong>'
    }

    for field, display_field_name in fields.items():
        if field == "activity_level":
            level = user_data['activity_level']['level']
            level_name = user_data['activity_level']['name']
            level_description = user_data['activity_level']['description']
            formatted_data.append(f"{display_field_name}: {level} ({level_name})\n{level_description}")
            continue
        value = user_data.get(field, "Не указано")
        formatted_data.append(f"{display_field_name}: {value}")

    return "\n\n".join(formatted_data)


async def update_user(user_data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{API_URL}/user/update/{user_data['id']}", json=user_data) as response:
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()


async def get_activity_level_id(level: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/level/get/{level}") as response:
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()
            data = await response.json()
            return data['id']


async def get_activity_levels():
    async with aiohttp.ClientSession() as session:
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
    async with aiohttp.ClientSession() as session:
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
