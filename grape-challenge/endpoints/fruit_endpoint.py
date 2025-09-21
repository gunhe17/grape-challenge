"""
Fruit domain endpoint helpers
"""
from typing import Optional, Dict, Any, List
from usecases import fruit


def api_create_fruit_template(name: str, type: str = 'normal', status_images: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """새 과일 템플릿 생성 API (Admin)"""
    command = fruit.CreateFruitTemplateCommand(name=name, type=type, status_images=status_images)
    return fruit.create_fruit_template_admin(command)


def api_get_fruit_templates() -> List[Dict[str, Any]]:
    """과일 템플릿 목록 조회 API"""
    query = fruit.GetAllFruitTemplatesQuery()
    return fruit.get_fruit_template_list(query)


def api_get_fruit_template(template_id: str) -> Optional[Dict[str, Any]]:
    """과일 템플릿 조회 API"""
    query = fruit.GetFruitTemplateQuery(template_id=template_id)
    return fruit.get_fruit_template_info(query)


def api_update_fruit_template(template_id: str, name: Optional[str] = None,
                             type: Optional[str] = None,
                             status_images: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
    """템플릿 정보 수정 API (Admin)"""
    command = fruit.UpdateFruitTemplateCommand(
        template_id=template_id,
        name=name,
        type=type,
        status_images=status_images
    )
    return fruit.update_fruit_template_admin(command)


def api_create_fruit(template_id: str, status: str = 'first') -> Dict[str, Any]:
    """과일 생성 API"""
    command = fruit.CreateFruitCommand(template_id=template_id, status=status)
    return fruit.create_fruit(command)


def api_get_fruit(fruit_id: str) -> Optional[Dict[str, Any]]:
    """보유 과일 조회 API"""
    query = fruit.GetFruitQuery(fruit_id=fruit_id)
    return fruit.get_owned_fruit(query)


def api_update_fruit_status(fruit_id: str, status: str) -> Optional[Dict[str, Any]]:
    """과일 상태 변경 API"""
    command = fruit.UpdateFruitStatusCommand(fruit_id=fruit_id, status=status)
    return fruit.change_fruit_status(command)


def api_delete_fruit(fruit_id: str) -> bool:
    """과일 삭제 API"""
    command = fruit.DeleteFruitCommand(fruit_id=fruit_id)
    return fruit.remove_fruit(command)