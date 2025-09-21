from typing import Optional, List, Dict, Any
from database.database_json import json_db

MISSION_TABLE_NAME = "missions"
MISSION_TEMPLATE_TABLE_NAME = "mission_templates"

# Mission Template Domain
def create_mission_template(name: str, type: str = 'normal', content: str = '') -> Dict[str, Any]:
    """미션 템플릿 생성 (Admin)"""
    template_data = {
        "name": name,
        "type": type,
        "content": content
    }
    return json_db.insert(MISSION_TEMPLATE_TABLE_NAME, template_data)

def get_all_mission_templates() -> List[Dict[str, Any]]:
    """미션 템플릿 목록 조회"""
    return json_db.get_table(MISSION_TEMPLATE_TABLE_NAME)

def get_mission_template_by_id(template_id: str) -> Optional[Dict[str, Any]]:
    """미션 템플릿 조회"""
    return json_db.find_one(MISSION_TEMPLATE_TABLE_NAME, id=template_id)

def update_mission_template(template_id: str, **kwargs) -> Optional[Dict[str, Any]]:
    """템플릿 내용 수정 (Admin)"""
    return json_db.update(MISSION_TEMPLATE_TABLE_NAME, template_id, kwargs)

# Mission Domain
def create_mission(template_id: str) -> Dict[str, Any]:
    """미션 생성"""
    mission_data = {
        "template_id": template_id,
        "completed_at": None
    }
    return json_db.insert(MISSION_TABLE_NAME, mission_data)

def get_mission_by_id(mission_id: str) -> Optional[Dict[str, Any]]:
    """미션 조회"""
    return json_db.find_one(MISSION_TABLE_NAME, id=mission_id)

def get_all_missions() -> List[Dict[str, Any]]:
    """모든 미션 조회 (workflow에서 사용)"""
    return json_db.get_table(MISSION_TABLE_NAME)

def update_mission(mission_id: str, **kwargs) -> Optional[Dict[str, Any]]:
    """미션 업데이트 (workflow에서 사용)"""
    return json_db.update(MISSION_TABLE_NAME, mission_id, kwargs)

def delete_mission(mission_id: str) -> bool:
    """미션 삭제"""
    return json_db.delete(MISSION_TABLE_NAME, mission_id)