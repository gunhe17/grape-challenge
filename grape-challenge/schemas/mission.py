from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MissionBase(BaseModel):
    template_id: int
    user_id: int
    status: str = 'pending'

class MissionCreate(MissionBase):
    pass

class MissionUpdate(BaseModel):
    template_id: Optional[int] = None
    status: Optional[str] = None

class MissionRead(MissionBase):
    id: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class MissionComplete(BaseModel):
    completed_at: Optional[datetime] = None

class MissionTemplateBase(BaseModel):
    name: str
    type: str = 'normal'
    content: str

class MissionTemplateCreate(MissionTemplateBase):
    pass

class MissionTemplateUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    content: Optional[str] = None

class MissionTemplateRead(MissionTemplateBase):
    id: int
    
    class Config:
        from_attributes = True

class MissionCompleteResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    mission_count: Optional[int] = None
    session_completed: Optional[bool] = None
    new_session_created: Optional[bool] = None