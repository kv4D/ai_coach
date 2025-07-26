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
