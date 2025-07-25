import requests


API_URL = 'http://localhost:8000/'


def create_user(user_data: dict):
    user_data['activity_level_id'] = get_activity_level_id(user_data["activity_level"])
    response = requests.post(f"{API_URL}/user/create", json=user_data)

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Details:", response.text)
        response.raise_for_status()                  
        
    
    print(response.json())
    return response.json()


def get_activity_level_id(level: int):
    response = requests.get(f"{API_URL}/level/get/{level}",)
    
    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Details:", response.text)
        response.raise_for_status()         
    return response.json()['id']

def get_activity_levels():
    response = requests.get(f"{API_URL}/level/all")

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Details:", response.text)
        response.raise_for_status()  
        
    levels = sorted([level['level'] for level in response.json()])                


def get_activity_levels_descriptions():
    response = requests.get(f"{API_URL}/level/all")

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Details:", response.text)
        response.raise_for_status()  
        
    levels = {}
    for level in response.json():
        levels[level['level']] = level['description']
