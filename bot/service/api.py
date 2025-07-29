import aiohttp
from models.activity_level import ActivityLevel
from models.user import User


API_URL = 'http://localhost:8000'


async def create_user(user: User):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/user/get/{user.id}") as response:
            if response.status == 200:
                return await update_user(user)

        async with session.post(f"{API_URL}/user/create", json=user.model_dump()) as response:
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()


async def get_user(user_id: int) -> User:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/user/get/{user_id}") as response:
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()

            user_data = await response.json()
            user = User(**user_data)
            return user


def render_user_data(user_data: dict) -> str:
    """Transform user data dictionary into a formatted string for display."""
    formatted_data = []
    
    # field names to show
    fields = {
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


async def update_user(user: User):
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{API_URL}/user/update/{user.id}", json=user.model_dump()) as response:
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()


async def get_activity_level(level: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/level/get/{level}") as response:
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()
            data = await response.json()
            activity_level = ActivityLevel(**data)
            return activity_level


async def get_activity_levels() -> list[int]:
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

async def get_user_training_plan(user_id: int) -> str | None:
    """Get user's training plan from API's database."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/plan/get/user/{user_id}") as response:
            if response.status == 404:
                return None
            if response.status != 200:
                text = await response.text()
                print("Status code:", response.status)
                print("Details:", text)
                response.raise_for_status()
            
            data = await response.json()
            plan = data['plan_description']
            return plan
