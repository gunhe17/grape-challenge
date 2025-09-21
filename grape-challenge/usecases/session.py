from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from repositories import session as session_repo

# 세션 시작
@dataclass
class CreateSessionCommand:
    user_id: str

def start_session(command: CreateSessionCommand) -> Dict[str, Any]:
    """세션 시작"""
    session = session_repo.create_session(command.user_id)
    return {
        "id": session["id"],
        "user_id": session["user_id"],
        "fruit_id": session.get("fruit_id"),
        "mission_ids": session.get("mission_ids", []),
        "status": session["status"],
        "created_at": session.get("created_at"),
        "updated_at": session.get("updated_at")
    }

# 현재 세션 상태 조회
@dataclass
class GetSessionStatusQuery:
    user_id: str

def get_current_session_status(query: GetSessionStatusQuery) -> Optional[Dict[str, Any]]:
    """현재 세션 상태 조회"""
    session = session_repo.get_session_by_user_and_status(query.user_id, "in progress")
    if not session:
        return None

    return {
        "id": session["id"],
        "user_id": session["user_id"],
        "fruit_id": session.get("fruit_id"),
        "mission_ids": session.get("mission_ids", []),
        "status": session["status"],
        "created_at": session.get("created_at"),
        "updated_at": session.get("updated_at")
    }

# 진행 중인 세션 조회
def get_in_progress_session(query: GetSessionStatusQuery) -> Optional[Dict[str, Any]]:
    """진행 중인 세션 조회"""
    return get_current_session_status(query)

# 사용자의 세션 목록 조회
@dataclass
class GetUserSessionsQuery:
    user_id: str
    status: Optional[str] = None

def get_user_sessions(query: GetUserSessionsQuery) -> List[Dict[str, Any]]:
    """사용자의 세션 목록 조회 (상태별 필터링 가능)"""
    sessions = session_repo.get_sessions_by_user(query.user_id, query.status)
    return [
        {
            "id": session["id"],
            "user_id": session["user_id"],
            "fruit_id": session.get("fruit_id"),
            "mission_ids": session.get("mission_ids", []),
            "status": session["status"],
            "created_at": session.get("created_at"),
            "updated_at": session.get("updated_at")
        }
        for session in sessions
    ]

# 미션 완료 시 mission_ids 추가, 상태 변경
@dataclass
class UpdateSessionCommand:
    session_id: str
    mission_ids: Optional[List[str]] = None
    status: Optional[str] = None
    fruit_id: Optional[str] = None

def update_session_on_mission_complete(command: UpdateSessionCommand) -> Optional[Dict[str, Any]]:
    """미션 완료 시 mission_ids 추가, 상태 변경"""
    update_data = {}

    if command.mission_ids is not None:
        update_data["mission_ids"] = command.mission_ids
    if command.status is not None:
        update_data["status"] = command.status
    if command.fruit_id is not None:
        update_data["fruit_id"] = command.fruit_id

    session = session_repo.update_session(command.session_id, **update_data)
    if not session:
        return None

    return {
        "id": session["id"],
        "user_id": session["user_id"],
        "fruit_id": session.get("fruit_id"),
        "mission_ids": session.get("mission_ids", []),
        "status": session["status"],
        "created_at": session.get("created_at"),
        "updated_at": session.get("updated_at")
    }