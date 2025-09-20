from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from ..repositories.session_repository import SessionRepository
from ..routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/api/sessions", tags=["sessions"])
session_repo = SessionRepository()

class SessionCreate(BaseModel):
    user_id: int
    fruit_id: Optional[int] = None

class SessionMissionUpdate(BaseModel):
    mission_ids: List[int]

class SessionStatusUpdate(BaseModel):
    status: str

@router.post("/")
def create_session(
    session: SessionCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    if session.user_id != current_user["id"] and current_user["role"] != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    return session_repo.create_session(session.user_id, session.fruit_id)

@router.get("/user/{user_id}")
def get_user_session(
    user_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    if user_id != current_user["id"] and current_user["role"] != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    
    session = session_repo.get_by_user_id(user_id)
    if not session:
        raise HTTPException(status_code=404, detail="No active session found")
    return session

@router.get("/")
def get_all_sessions(current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user["role"] != 'admin':
        return session_repo.get_by_user_id(current_user["id"])
    else:
        return session_repo.get_all_sessions()

@router.patch("/{session_id}/missions")
def update_session_missions(
    session_id: int,
    mission_update: SessionMissionUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    session = session_repo.get_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.get("user_id") != current_user["id"] and current_user["role"] != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_session = session_repo.update_mission_ids(session_id, mission_update.mission_ids)
    return updated_session

@router.patch("/{session_id}/status")
def update_session_status(
    session_id: int,
    status_update: SessionStatusUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    session = session_repo.get_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.get("user_id") != current_user["id"] and current_user["role"] != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_session = session_repo.update_status(session_id, status_update.status)
    return updated_session