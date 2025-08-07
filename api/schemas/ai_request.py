from typing import Optional
from pydantic import BaseModel

class UserAIRequest(BaseModel):
    user_id: int
    content: Optional[str] = None
