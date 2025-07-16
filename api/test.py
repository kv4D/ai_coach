from asyncio import run
from service.user import get_all


all_users = run(get_all())
for i in all_users:
    print(i)