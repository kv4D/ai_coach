"""AI API requests Pydantic schemas."""
from typing import Optional
from pydantic import BaseModel


class UserAIRequest(BaseModel):
    """Schema for request from a certain user."""
    user_id: int
    content: Optional[str] = None
