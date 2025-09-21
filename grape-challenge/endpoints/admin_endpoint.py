"""
Admin domain endpoint helpers
"""
from typing import Dict, Any
from .user_endpoint import api_get_all_users
from .session_endpoint import api_get_user_sessions


def api_get_admin_statistics() -> Dict[str, Any]:
    """Admin 대시보드 통계 API"""
    users = api_get_all_users()

    # 간단한 통계 계산
    total_users = len(users)

    # 각 사용자별 세션 통계 계산
    user_stats = []
    for user_data in users:
        user_sessions = api_get_user_sessions(user_data['id'])
        completed_sessions = [s for s in user_sessions if s['status'] == 'completed']

        user_stats.append({
            "id": user_data["id"],
            "name": user_data["name"],
            "cell": user_data["cell"],
            "role": user_data["role"],
            "statistics": {
                "total_sessions": len(user_sessions),
                "completed_sessions": len(completed_sessions)
            }
        })

    return {
        "total_users": total_users,
        "users": user_stats
    }