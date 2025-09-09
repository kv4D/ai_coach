"""Endpoints for User."""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.user import User, UserInput, UserUpdate
from api.schemas.ai_request import UserAIRequest
from api.database.database import get_db_session
from api.service import user as service


router = APIRouter(prefix="/user")


@router.post('/create')
async def create_user(user_data: UserInput,
                      session: AsyncSession = Depends(get_db_session)) -> None:
    """Create a new user."""
    await service.create(user_data, session=session)


@router.post('/chat')
async def chat_with_ai(request: UserAIRequest,
                       session: AsyncSession = Depends(get_db_session)) -> str:
    """Send message to AI.

    AI-coach will take user's request, analyze data about the user
    and send an answer (advise, help, etc.).
    """
    return await service.get_ai_answer(request, session=session)


@router.get('/get/{user_id}')
async def get_by_id(user_id: int,
                    session: AsyncSession = Depends(get_db_session)) -> User:
    """Get the user by ID."""
    user = await service.get_by_id(user_id, session=session)
    return user


@router.get('/all')
async def get_all(session: AsyncSession = Depends(get_db_session)) -> list[User]:
    """Get all users in the database."""
    users = await service.get_all(session=session)
    return users


@router.patch('/update/{user_id}')
async def update_user(user_id: int,
                      user_data: UserUpdate,
                      session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    """Update the user by their ID."""
    await service.update(user_id, user_data, session)
    return JSONResponse(status_code=200,
                        content={"message": f"User with ID={user_id} was updated"})


@router.delete('/delete/{user_id}')
async def delete_user(user_id: int,
                      session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    """Delete the user by their ID."""
    await service.delete(user_id, session=session)
    return JSONResponse(status_code=200,
                        content={"message": f"User with ID={user_id} was deleted"})
