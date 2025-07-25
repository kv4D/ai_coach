import requests


API_URL = 'http://localhost:8000/'


def create_user(user_data: dict):
    response = requests.post(f"{API_URL}/user/create", json=user_data)

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Details:", response.text)
        response.raise_for_status()                    

    return response.json()


def get_activity_levels():
    response = requests.get(f"{API_URL}/level/all")

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Details:", response.text)
        response.raise_for_status()  
        
    levels = sorted([level['level'] for level in response.json()])                
    print(levels)


def get_activity_levels_descriptions():
    response = requests.get(f"{API_URL}/level/all")

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Details:", response.text)
        response.raise_for_status()  
        
    levels = {}
    for level in response.json():
        levels[level['level']] = level['description']
    print(levels)
