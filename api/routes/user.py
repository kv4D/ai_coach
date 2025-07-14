from fastapi import APIRouter
from schemas.user import User


router = APIRouter(prefix=f"/user")


@router.get('')
def ping() -> str:
    """Test endpoint"""
    return 'hello, User'

@router.post('/create')
def create(user: User):
    """Create new user"""
    return None

@router.get('/get/{id}')
def get_by_id(id: int):
    """Get a user by id"""
    return None