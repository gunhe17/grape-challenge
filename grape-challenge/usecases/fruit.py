from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from repositories import fruit as fruit_repo

# 새 과일 템플릿 생성 (Admin)
@dataclass
class CreateFruitTemplateCommand:
    name: str
    type: str = 'normal'
    status_images: Optional[Dict[str, str]] = None

def create_fruit_template_admin(command: CreateFruitTemplateCommand) -> Dict[str, Any]:
    """새 과일 템플릿 생성 (Admin)"""
    template = fruit_repo.create_fruit_template(
        command.name,
        command.type,
        command.status_images
    )
    return {
        "id": template["id"],
        "name": template["name"],
        "type": template["type"],
        "status_images": template.get("status_images", {}),
        "created_at": template.get("created_at"),
        "updated_at": template.get("updated_at")
    }

# 과일 템플릿 목록 조회
@dataclass
class GetAllFruitTemplatesQuery:
    pass

def get_fruit_template_list(_query: GetAllFruitTemplatesQuery) -> List[Dict[str, Any]]:
    """과일 템플릿 목록 조회"""
    templates = fruit_repo.get_all_fruit_templates()
    return [
        {
            "id": template["id"],
            "name": template["name"],
            "type": template["type"],
            "status_images": template.get("status_images", {}),
            "created_at": template.get("created_at"),
            "updated_at": template.get("updated_at")
        }
        for template in templates
    ]

# 과일 템플릿 조회
@dataclass
class GetFruitTemplateQuery:
    template_id: str

def get_fruit_template_info(query: GetFruitTemplateQuery) -> Optional[Dict[str, Any]]:
    """과일 템플릿 조회"""
    template = fruit_repo.get_fruit_template_by_id(query.template_id)
    if not template:
        return None

    return {
        "id": template["id"],
        "name": template["name"],
        "type": template["type"],
        "status_images": template.get("status_images", {}),
        "created_at": template.get("created_at"),
        "updated_at": template.get("updated_at")
    }

# 템플릿 정보 수정 (Admin)
@dataclass
class UpdateFruitTemplateCommand:
    template_id: str
    name: Optional[str] = None
    type: Optional[str] = None
    status_images: Optional[Dict[str, str]] = None

def update_fruit_template_admin(command: UpdateFruitTemplateCommand) -> Optional[Dict[str, Any]]:
    """템플릿 정보 수정 (Admin)"""
    update_data = {}

    if command.name is not None:
        update_data["name"] = command.name
    if command.type is not None:
        update_data["type"] = command.type
    if command.status_images is not None:
        update_data["status_images"] = command.status_images

    template = fruit_repo.update_fruit_template(command.template_id, **update_data)
    if not template:
        return None

    return {
        "id": template["id"],
        "name": template["name"],
        "type": template["type"],
        "status_images": template.get("status_images", {}),
        "created_at": template.get("created_at"),
        "updated_at": template.get("updated_at")
    }

# 과일 생성
@dataclass
class CreateFruitCommand:
    template_id: str
    status: str = 'first'

def create_fruit(command: CreateFruitCommand) -> Dict[str, Any]:
    """과일 생성"""
    fruit = fruit_repo.create_fruit(command.template_id, command.status)
    return {
        "id": fruit["id"],
        "template_id": fruit["template_id"],
        "status": fruit["status"],
        "created_at": fruit.get("created_at"),
        "updated_at": fruit.get("updated_at")
    }

# 보유 과일 조회
@dataclass
class GetFruitQuery:
    fruit_id: str

def get_owned_fruit(query: GetFruitQuery) -> Optional[Dict[str, Any]]:
    """보유 과일 조회"""
    fruit = fruit_repo.get_fruit_by_id(query.fruit_id)
    if not fruit:
        return None

    return {
        "id": fruit["id"],
        "template_id": fruit["template_id"],
        "status": fruit["status"],
        "created_at": fruit.get("created_at"),
        "updated_at": fruit.get("updated_at")
    }

# 과일 상태 변경
@dataclass
class UpdateFruitStatusCommand:
    fruit_id: str
    status: str

def change_fruit_status(command: UpdateFruitStatusCommand) -> Optional[Dict[str, Any]]:
    """과일 상태 변경"""
    fruit = fruit_repo.update_fruit_status(command.fruit_id, command.status)
    if not fruit:
        return None

    return {
        "id": fruit["id"],
        "template_id": fruit["template_id"],
        "status": fruit["status"],
        "created_at": fruit.get("created_at"),
        "updated_at": fruit.get("updated_at")
    }

# 과일 삭제
@dataclass
class DeleteFruitCommand:
    fruit_id: str

def remove_fruit(command: DeleteFruitCommand) -> bool:
    """과일 삭제"""
    return fruit_repo.delete_fruit(command.fruit_id)