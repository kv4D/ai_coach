from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import User
from db.database import get_db_session
from service import user as service


router = APIRouter(prefix=f"/user")


@router.get('')
def ping() -> str:
    """Test endpoint"""
    return 'Hello, User'

@router.post('/create')
async def create_user(user_data: User,
                      session: AsyncSession = Depends(get_db_session)):
    """Create new user"""
    response = await service.create(user_data.model_dump(), session=session)
    return response

@router.get('/get/{id}')
async def get_by_id(id: int, 
                    session: AsyncSession = Depends(get_db_session)):
    """Get a user by id"""
    user = await service.get_by_id(id, session=session)
    return user

@router.get('/all')
async def get_all(session: AsyncSession = Depends(get_db_session)):
    """Get a user by id"""
    users = await service.get_all(session=session)
    return users