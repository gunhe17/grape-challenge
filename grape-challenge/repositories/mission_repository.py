from typing import Optional, List, Dict, Any
from datetime import datetime, date
from ..database.database_json import json_db
import random

class MissionRepository:
    def __init__(self):
        self.table_name = "missions"
    
    def create_mission(self, template_id: int, user_id: int, status: str = 'pending') -> Dict[str, Any]:
        mission_data = {
            "template_id": template_id,
            "user_id": user_id,
            "status": status
        }
        return json_db.insert(self.table_name, mission_data)
    
    def get_by_id(self, mission_id: int) -> Optional[Dict[str, Any]]:
        mission = json_db.find_one(self.table_name, id=mission_id)
        if mission and mission.get('template_id'):
            template_repo = MissionTemplateRepository()
            template = template_repo.get_by_id(mission['template_id'])
            mission['template'] = template
        return mission
    
    def get_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        missions = json_db.find(self.table_name, user_id=user_id)

        # 템플릿 정보를 함께 조회하여 추가
        template_repo = MissionTemplateRepository()
        for mission in missions:
            if mission.get('template_id'):
                template = template_repo.get_by_id(mission['template_id'])
                mission['template'] = template

        return missions
    
    def get_today_missions(self, user_id: int) -> List[Dict[str, Any]]:
        today = date.today().isoformat()
        missions = json_db.find(self.table_name, user_id=user_id)
        today_missions = [m for m in missions if m.get('created_at', '').startswith(today)]

        # 템플릿 정보를 함께 조회하여 추가
        template_repo = MissionTemplateRepository()

        for mission in today_missions:
            if mission.get('template_id'):
                template = template_repo.get_by_id(mission['template_id'])
                mission['template'] = template

        return today_missions
    
    def check_daily_limit(self, user_id: int) -> bool:
        today = date.today().isoformat()
        missions = json_db.find(self.table_name, user_id=user_id, status='completed')
        completed_today = any(m.get('completed_at', '').startswith(today) for m in missions)
        return not completed_today
    
    def complete_mission(self, mission_id: int) -> Optional[Dict[str, Any]]:
        mission = self.get_by_id(mission_id)
        if mission and mission.get('status') == 'pending':
            updates = {
                "status": "completed",
                "completed_at": datetime.now().isoformat()
            }
            return json_db.update(self.table_name, mission_id, updates)
        return mission
    
    def get_completed_missions(self, user_id: int) -> List[Dict[str, Any]]:
        return json_db.find(self.table_name, user_id=user_id, status='completed')
    
    def update(self, mission_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        return json_db.update(self.table_name, mission_id, kwargs)
    
    def delete(self, mission_id: int) -> bool:
        return json_db.delete(self.table_name, mission_id)

class MissionTemplateRepository:
    def __init__(self):
        self.table_name = "mission_templates"
    
    def create_template(self, name: str, type: str = 'normal', content: str = '') -> Dict[str, Any]:
        template_data = {
            "name": name,
            "type": type,
            "content": content
        }
        return json_db.insert(self.table_name, template_data)
    
    def get_by_id(self, template_id: int) -> Optional[Dict[str, Any]]:
        return json_db.find_one(self.table_name, id=template_id)
    
    def get_by_type(self, type: str) -> List[Dict[str, Any]]:
        return json_db.find(self.table_name, type=type)
    
    def get_random_template(self, type: str = 'normal') -> Optional[Dict[str, Any]]:
        templates = self.get_by_type(type)
        return random.choice(templates) if templates else None
    
    def get_all_templates(self) -> List[Dict[str, Any]]:
        return json_db.get_table(self.table_name)
    
    def update_template(self, template_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        return json_db.update(self.table_name, template_id, kwargs)
    
    def delete(self, template_id: int) -> bool:
        return json_db.delete(self.table_name, template_id)