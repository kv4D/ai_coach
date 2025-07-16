from . base import BaseCRUD
from db.models import User


class UserCRUD(BaseCRUD):
    _model = User