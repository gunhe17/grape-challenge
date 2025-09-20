from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from ..repositories.fruit_repository import FruitRepository, FruitTemplateRepository
from ..repositories.session_repository import SessionRepository

class FruitService:
    def __init__(self):
        self.fruit_repo = FruitRepository()
        self.fruit_template_repo = FruitTemplateRepository()
        self.session_repo = SessionRepository()
    
    def get_fruit_image_by_progress(self, db: Session, user_id: int) -> Optional[Dict]:
        session = self.session_repo.get_active_session(user_id)
        if not session or not session.get('fruit_id'):
            return None

        fruit = self.fruit_repo.get_by_id(session['fruit_id'])
        if not fruit:
            return None

        template = self.fruit_template_repo.get_by_id(fruit['template_id'])
        if not template:
            return None

        mission_ids = session.get('mission_ids', [])
        mission_count = len(mission_ids)
        
        image_mapping = {
            0: template.get('seed_image'),
            1: template.get('seed_image'),
            2: template.get('germination_image'),
            3: template.get('seedling_image'),
            4: template.get('juvenile_image'),
            5: template.get('vegetative_image'),
            6: template.get('reproductive_image'),
            7: template.get('fruiting_image')
        }

        current_image = image_mapping.get(mission_count, template.get('seed_image'))
        growth_stage = self.calculate_growth_stage(mission_count)
        
        return {
            "fruit_id": fruit.get('id'),
            "template_id": template.get('id'),
            "template_name": template.get('name'),
            "current_image": current_image,
            "growth_stage": growth_stage,
            "mission_count": mission_count,
            "progress_percentage": (mission_count / 7) * 100
        }
    
    def calculate_growth_stage(self, mission_count: int) -> str:
        stages = {
            0: "씨앗",
            1: "씨앗",
            2: "발아",
            3: "새싹",
            4: "성장",
            5: "개화",
            6: "결실",
            7: "열매"
        }
        return stages.get(mission_count, "씨앗")
    
    def get_user_fruits(self, db: Session, user_id: int) -> List[Dict]:
        sessions = self.session_repo.get_by_user_id(user_id)
        fruits = []
        
        for session in sessions:
            if session.get('status') == 'completed' and session.get('fruit_id'):
                fruit = self.fruit_repo.get_by_id(session['fruit_id'])
                if fruit:
                    template = self.fruit_template_repo.get_by_id(fruit['template_id'])
                    if template:
                        fruits.append({
                            "fruit_id": fruit.get('id'),
                            "template_name": template.get('name'),
                            "template_type": template.get('type'),
                            "status": fruit.get('status'),
                            "image": template.get('fruiting_image'),
                            "created_at": fruit.get('created_at')
                        })
        
        return fruits
    
    def create_new_fruit(self, db: Session, template_id: int) -> Dict[str, Any]:
        return self.fruit_repo.create_fruit(template_id=template_id)

    def update_fruit_status(self, db: Session, fruit_id: int, status: str) -> Optional[Dict[str, Any]]:
        return self.fruit_repo.update_status(fruit_id, status)

    def get_all_templates(self, db: Session) -> List[Dict[str, Any]]:
        return self.fruit_template_repo.get_all_templates()
    
    def get_template_by_id(self, db: Session, template_id: int) -> Optional[Dict[str, Any]]:
        return self.fruit_template_repo.get_by_id(template_id)