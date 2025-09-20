from typing import Optional, List, Dict, Any
from ..database.database_json import json_db
import json

class SessionRepository:
    def __init__(self):
        self.table_name = "sessions"
    
    def create_session(self, user_id: int, fruit_id: Optional[int] = None) -> Dict[str, Any]:
        session_data = {
            "user_id": user_id,
            "fruit_id": fruit_id,
            "mission_ids": [],
            "status": "active"
        }
        return json_db.insert(self.table_name, session_data)
    
    def get_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        return json_db.find(self.table_name, user_id=user_id)
    
    def get_active_session(self, user_id: int) -> Optional[Dict[str, Any]]:
        sessions = json_db.find(self.table_name, user_id=user_id, status="active")
        return sessions[0] if sessions else None
    
    def get_by_id(self, session_id: int) -> Optional[Dict[str, Any]]:
        return json_db.find_one(self.table_name, id=session_id)
    
    def update_mission_ids(self, session_id: int, mission_ids: List[int]) -> Optional[Dict[str, Any]]:
        return json_db.update(self.table_name, session_id, {"mission_ids": mission_ids})
    
    def add_mission_id(self, session_id: int, mission_id: int) -> Optional[Dict[str, Any]]:
        session = self.get_by_id(session_id)
        if session:
            mission_ids = session.get("mission_ids", [])
            if mission_id not in mission_ids:
                mission_ids.append(mission_id)
                return json_db.update(self.table_name, session_id, {"mission_ids": mission_ids})
        return session
    
    def update_status(self, session_id: int, status: str) -> Optional[Dict[str, Any]]:
        return json_db.update(self.table_name, session_id, {"status": status})
    
    def complete_session(self, session_id: int) -> Optional[Dict[str, Any]]:
        return self.update_status(session_id, 'completed')
    
    def update(self, session_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        return json_db.update(self.table_name, session_id, kwargs)
    
    def delete(self, session_id: int) -> bool:
        return json_db.delete(self.table_name, session_id)
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        return json_db.get_table(self.table_name)