"""Endpoints for User."""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import User, UserInput, UserUpdate
from db.database import get_db_session
from service import user as service


router = APIRouter(prefix=f"/user")


@router.post('/create')
async def create_user(user_data: UserInput,
                      session: AsyncSession = Depends(get_db_session)) -> User | None:
    """Create a new user.

    Args:
        user_data (`UserInput`): 
        session (`AsyncSession`): an asynchronous database session
    """
    user = await service.create(user_data, session=session)
    return user

@router.get('/get/{user_id}')
async def get_by_id(user_id: int, 
                    session: AsyncSession = Depends(get_db_session)) -> User:
    """Get the user by ID.
    
    Args:
        user_id (`int`)
        session (`AsyncSession`): an asynchronous database session
    """
    user = await service.get_by_id(user_id, session=session)
    return user

@router.get('/all')
async def get_all(session: AsyncSession = Depends(get_db_session)) -> list[User]:
    """Get all users in the database.  
    
    Args:
        session (`AsyncSession`): an asynchronous database session
    """
    users = await service.get_all(session=session)
    return users

@router.patch('/update/{user_id}')
async def update_user(user_id: int, 
                      user_data: UserUpdate,
                      session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    """Update the user by their ID.
        
    Args:
        user_id (`int`)
        user_data (`UserUpdate`): new data for the user
        session (`AsyncSession`): an asynchronous database session
    """
    await service.update(user_id, user_data, session)
    return JSONResponse(status_code=200, 
                        content={"message": f"User with ID={id} was updated"})

@router.delete('/delete/{user_id}')
async def delete_user(user_id: int,
                      session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    """Delete the user by their ID.
            
    Args:
        user_id (`int`)
        session (`AsyncSession`): an asynchronous database session
    """
    await service.delete(user_id, session=session)
    return JSONResponse(status_code=200, 
                        content={"message": f"User with ID={id} was deleted"})