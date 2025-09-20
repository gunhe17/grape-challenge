from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    name: str
    cell: str

class LoginResponse(BaseModel):
    success: bool
    access_token: str
    token_type: str
    user_id: int
    name: str
    cell: str
    role: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    name: Optional[str] = None
    role: Optional[str] = None