import requests


API_URL = 'http://localhost:8000/'


def create_user(user_data: dict):
    # check for user
    response = requests.get(f"{API_URL}/user/get/{user_data['id']}")
    if response.status_code == 200:
        return update_user(user_data)
    user_data['activity_level_id'] = get_activity_level_id(user_data["activity_level"])
    response = requests.post(f"{API_URL}/user/create", json=user_data)

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Details:", response.text)
        response.raise_for_status()                  

def update_user(user_data: dict):
    response = requests.patch(f"{API_URL}/user/update/{user_data['id']}", json=user_data)

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Details:", response.text)
        response.raise_for_status()   


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
    return levels


def get_activity_levels_descriptions():
    response = requests.get(f"{API_URL}/level/all")

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Details:", response.text)
        response.raise_for_status()  
        
    descriptions_by_level = {}
    for level in response.json():
        descriptions_by_level[level['level']] = level['description']
    return descriptions_by_level
