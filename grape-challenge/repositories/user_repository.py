from typing import Optional, Dict, Any, List
from ..database.database_json import json_db

class UserRepository:
    def __init__(self):
        self.table_name = "users"
    
    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        return json_db.find_one(self.table_name, name=name)
    
    def get_by_name_and_cell(self, name: str, cell: str) -> Optional[Dict[str, Any]]:
        """이름과 셀 이름으로 사용자 조회"""
        users = json_db.get_table(self.table_name)
        for user in users:
            if user.get('name') == name and user.get('cell') == cell:
                return user
        return None
    
    def create_user(self, name: str, cell: str, role: str = 'user') -> Dict[str, Any]:
        user_data = {
            "name": name,
            "cell": cell,
            "role": role
        }
        return json_db.insert(self.table_name, user_data)
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        return json_db.get_table(self.table_name)
    
    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        return json_db.find_one(self.table_name, id=user_id)
    
    def update_user(self, user_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        return json_db.update(self.table_name, user_id, kwargs)
    
    def delete_user(self, user_id: int) -> bool:
        return json_db.delete(self.table_name, user_id)