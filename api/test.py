from asyncio import run
from service.user import get_by_id
from schemas.user import User


all_users = run(get_by_id(2000))
print(all_users)