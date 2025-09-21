"""
Session domain endpoint helpers
"""
from typing import Optional, Dict, Any, List
from usecases import session


def api_start_session(user_id: str) -> Dict[str, Any]:
    """세션 시작 API"""
    command = session.CreateSessionCommand(user_id=user_id)
    return session.start_session(command)


def api_get_current_session(user_id: str) -> Optional[Dict[str, Any]]:
    """현재 세션 상태 조회 API"""
    query = session.GetSessionStatusQuery(user_id=user_id)
    return session.get_current_session_status(query)


def api_get_in_progress_session(user_id: str) -> Optional[Dict[str, Any]]:
    """진행 중인 세션 조회 API"""
    query = session.GetSessionStatusQuery(user_id=user_id)
    return session.get_in_progress_session(query)


def api_get_user_sessions(user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """사용자의 세션 목록 조회 API"""
    query = session.GetUserSessionsQuery(user_id=user_id, status=status)
    return session.get_user_sessions(query)