from typing import Optional, List, Dict, Any
from database.database_json import json_db

FRUIT_TABLE_NAME = "fruits"
FRUIT_TEMPLATE_TABLE_NAME = "fruit_templates"

# Fruit Template Domain
def create_fruit_template(name: str, type: str = 'normal', status_images: Dict[str, str] | None = None) -> Dict[str, Any]:
    """새 과일 템플릿 생성 (Admin)"""
    template_data = {
        "name": name,
        "type": type,
        "status_images": status_images or {}
    }
    return json_db.insert(FRUIT_TEMPLATE_TABLE_NAME, template_data)

def get_all_fruit_templates() -> List[Dict[str, Any]]:
    """과일 템플릿 목록 조회"""
    return json_db.get_table(FRUIT_TEMPLATE_TABLE_NAME)

def get_fruit_template_by_id(template_id: str) -> Optional[Dict[str, Any]]:
    """과일 템플릿 조회"""
    return json_db.find_one(FRUIT_TEMPLATE_TABLE_NAME, id=template_id)

def update_fruit_template(template_id: str, **kwargs) -> Optional[Dict[str, Any]]:
    """템플릿 정보 수정 (Admin)"""
    return json_db.update(FRUIT_TEMPLATE_TABLE_NAME, template_id, kwargs)

# Fruit Domain
def create_fruit(template_id: str, status: str = 'first') -> Dict[str, Any]:
    """과일 생성"""
    fruit_data = {
        "template_id": template_id,
        "status": status
    }
    return json_db.insert(FRUIT_TABLE_NAME, fruit_data)

def get_fruit_by_id(fruit_id: str) -> Optional[Dict[str, Any]]:
    """보유 과일 조회"""
    return json_db.find_one(FRUIT_TABLE_NAME, id=fruit_id)

def update_fruit_status(fruit_id: str, status: str) -> Optional[Dict[str, Any]]:
    """과일 상태 변경"""
    return json_db.update(FRUIT_TABLE_NAME, fruit_id, {"status": status})

def delete_fruit(fruit_id: str) -> bool:
    """과일 삭제"""
    return json_db.delete(FRUIT_TABLE_NAME, fruit_id)