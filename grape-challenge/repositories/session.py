from typing import Optional, List, Dict, Any
from database.database_json import json_db

TABLE_NAME = "sessions"

def create_session(user_id: str) -> Dict[str, Any]:
    """세션 시작"""
    session_data = {
        "user_id": user_id,
        "fruit_id": None,
        "mission_ids": [],
        "status": "in progress"
    }
    return json_db.insert(TABLE_NAME, session_data)

def get_session_by_user_and_status(user_id: str, status: str) -> Optional[Dict[str, Any]]:
    """현재 세션 상태 조회 / 진행 중인 세션 조회"""
    sessions = json_db.find(TABLE_NAME, user_id=user_id, status=status)
    return sessions[0] if sessions else None

def get_sessions_by_user(user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """사용자의 세션 목록 조회"""
    if status:
        return json_db.find(TABLE_NAME, user_id=user_id, status=status)
    return json_db.find(TABLE_NAME, user_id=user_id)

def update_session(session_id: str, **kwargs) -> Optional[Dict[str, Any]]:
    """미션 완료 시 mission_ids 추가, 상태 변경"""
    return json_db.update(TABLE_NAME, session_id, kwargs)

def get_session_by_id(session_id: str) -> Optional[Dict[str, Any]]:
    """세션 조회"""
    return json_db.find_one(TABLE_NAME, id=session_id)