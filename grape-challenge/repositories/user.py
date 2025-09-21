from typing import Optional, List, Dict, Any
from database.database_json import json_db

TABLE_NAME = "users"

def create_user(name: str, cell: str, role: str = 'user') -> Dict[str, Any]:
    """사용자 생성"""
    user_data = {
        "name": name,
        "cell": cell,
        "role": role
    }
    return json_db.insert(TABLE_NAME, user_data)

def get_user_by_login(name: str, cell: str) -> Optional[Dict[str, Any]]:
    """로그인 (name, cell)"""
    users = json_db.get_table(TABLE_NAME)
    for user in users:
        if user.get('name') == name and user.get('cell') == cell:
            return user
    return None

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """사용자 정보 조회"""
    return json_db.find_one(TABLE_NAME, id=user_id)

def get_all_users() -> List[Dict[str, Any]]:
    """(Admin) 사용자 전체 조회"""
    return json_db.get_table(TABLE_NAME)