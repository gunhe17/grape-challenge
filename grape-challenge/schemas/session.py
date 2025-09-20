from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class SessionBase(BaseModel):
    user_id: int
    fruit_id: Optional[int] = None

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    fruit_id: Optional[int] = None
    mission_ids: Optional[List[int]] = None
    status: Optional[str] = None

class SessionRead(SessionBase):
    id: int
    mission_ids: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SessionMissionUpdate(BaseModel):
    mission_ids: List[int]

class SessionStatusUpdate(BaseModel):
    status: str