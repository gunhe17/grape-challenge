from typing import Optional, List
from sqlalchemy.orm import Session
from ..repositories.mission_repository import MissionRepository, MissionTemplateRepository
from ..repositories.session_repository import SessionRepository
from ..repositories.fruit_repository import FruitRepository, FruitTemplateRepository

class MissionService:
    def __init__(self):
        self.mission_repo = MissionRepository()
        self.mission_template_repo = MissionTemplateRepository()
        self.session_repo = SessionRepository()
        self.fruit_repo = FruitRepository()
        self.fruit_template_repo = FruitTemplateRepository()
    
    def create_daily_mission(self, db: Session, user_id: int) -> Optional[dict]:
        if not self.mission_repo.check_daily_limit(user_id):
            return None

        template = self.mission_template_repo.get_random_template()
        if not template:
            return None

        mission = self.mission_repo.create_mission(
            template_id=template['id'],
            user_id=user_id
        )
        return mission
    
    def complete_mission(self, db: Session, user_id: int, mission_id: int) -> dict:
        if not self.mission_repo.check_daily_limit(user_id):
            return {"success": False, "message": "Daily limit reached"}

        mission = self.mission_repo.get_by_id(mission_id)
        if not mission or mission.get('user_id') != user_id:
            return {"success": False, "message": "Mission not found"}

        if mission.get('status') == 'completed':
            return {"success": False, "message": "Mission already completed"}

        completed_mission = self.mission_repo.complete_mission(mission_id)
        if not completed_mission:
            return {"success": False, "message": "Failed to complete mission"}

        session = self.session_repo.get_active_session(user_id)
        if not session:
            fruit_template = self.fruit_template_repo.get_all_templates()
            if fruit_template:
                fruit = self.fruit_repo.create_fruit(template_id=fruit_template[0]['id'])
                session = self.session_repo.create_session(user_id=user_id, fruit_id=fruit['id'])

        if session:
            self.session_repo.add_mission_id(session['id'], mission_id)
            mission_ids = session.get('mission_ids', [])
        else:
            mission_ids = []
        mission_count = len(mission_ids)
        
        new_session_created = False
        if mission_count >= 7 and session:
            self.session_repo.complete_session(session['id'])

            fruit_id = session.get('fruit_id')
            if fruit_id:
                self.fruit_repo.update_status(fruit_id, '열매')

            new_fruit_templates = self.fruit_template_repo.get_all_templates()
            if new_fruit_templates:
                new_fruit = self.fruit_repo.create_fruit(template_id=new_fruit_templates[0]['id'])
                new_session = self.session_repo.create_session(user_id=user_id, fruit_id=new_fruit['id'])
                new_session_created = True
        
        return {
            "success": True,
            "mission_count": mission_count,
            "session_completed": mission_count >= 7,
            "new_session_created": new_session_created
        }
    
    def get_user_missions(self, db: Session, user_id: int) -> List[dict]:
        return self.mission_repo.get_by_user_id(user_id)

    def get_today_missions(self, db: Session, user_id: int) -> List[dict]:
        return self.mission_repo.get_today_missions(user_id)

    def check_daily_completion(self, db: Session, user_id: int) -> bool:
        return not self.mission_repo.check_daily_limit(user_id)