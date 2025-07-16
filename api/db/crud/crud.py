from . base import BaseCRUD
from db.models import UserModel


class UserCRUD(BaseCRUD[UserModel]):
    _model = UserModel