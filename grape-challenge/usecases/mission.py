from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from repositories import mission as mission_repo

# 미션 템플릿 생성 (Admin)
@dataclass
class CreateMissionTemplateCommand:
    name: str
    type: str = 'normal'
    content: str = ''

def create_mission_template_admin(command: CreateMissionTemplateCommand) -> Dict[str, Any]:
    """미션 템플릿 생성 (Admin)"""
    template = mission_repo.create_mission_template(
        command.name,
        command.type,
        command.content
    )
    return {
        "id": template["id"],
        "name": template["name"],
        "type": template["type"],
        "content": template["content"],
        "created_at": template.get("created_at"),
        "updated_at": template.get("updated_at")
    }

# 미션 템플릿 목록 조회
@dataclass
class GetAllMissionTemplatesQuery:
    pass

def get_mission_template_list(query: GetAllMissionTemplatesQuery) -> List[Dict[str, Any]]:
    """미션 템플릿 목록 조회"""
    templates = mission_repo.get_all_mission_templates()
    return [
        {
            "id": template["id"],
            "name": template["name"],
            "type": template["type"],
            "content": template["content"],
            "created_at": template.get("created_at"),
            "updated_at": template.get("updated_at")
        }
        for template in templates
    ]

# 미션 템플릿 조회
@dataclass
class GetMissionTemplateQuery:
    template_id: str

def get_mission_template_info(query: GetMissionTemplateQuery) -> Optional[Dict[str, Any]]:
    """미션 템플릿 조회"""
    template = mission_repo.get_mission_template_by_id(query.template_id)
    if not template:
        return None

    return {
        "id": template["id"],
        "name": template["name"],
        "type": template["type"],
        "content": template["content"],
        "created_at": template.get("created_at"),
        "updated_at": template.get("updated_at")
    }

# 템플릿 내용 수정 (Admin)
@dataclass
class UpdateMissionTemplateCommand:
    template_id: str
    name: Optional[str] = None
    type: Optional[str] = None
    content: Optional[str] = None

def update_mission_template_admin(command: UpdateMissionTemplateCommand) -> Optional[Dict[str, Any]]:
    """템플릿 내용 수정 (Admin)"""
    update_data = {}

    if command.name is not None:
        update_data["name"] = command.name
    if command.type is not None:
        update_data["type"] = command.type
    if command.content is not None:
        update_data["content"] = command.content

    template = mission_repo.update_mission_template(command.template_id, **update_data)
    if not template:
        return None

    return {
        "id": template["id"],
        "name": template["name"],
        "type": template["type"],
        "content": template["content"],
        "created_at": template.get("created_at"),
        "updated_at": template.get("updated_at")
    }

# 미션 생성
@dataclass
class CreateMissionCommand:
    template_id: str

def create_mission(command: CreateMissionCommand) -> Dict[str, Any]:
    """미션 생성"""
    mission = mission_repo.create_mission(command.template_id)
    return {
        "id": mission["id"],
        "template_id": mission["template_id"],
        "completed_at": mission.get("completed_at"),
        "created_at": mission.get("created_at"),
        "updated_at": mission.get("updated_at")
    }

# 미션 조회
@dataclass
class GetMissionQuery:
    mission_id: str

def get_mission_info(query: GetMissionQuery) -> Optional[Dict[str, Any]]:
    """미션 조회"""
    mission = mission_repo.get_mission_by_id(query.mission_id)
    if not mission:
        return None

    return {
        "id": mission["id"],
        "template_id": mission["template_id"],
        "completed_at": mission.get("completed_at"),
        "created_at": mission.get("created_at"),
        "updated_at": mission.get("updated_at")
    }

# 미션 업데이트 (workflow에서 사용)
@dataclass
class UpdateMissionCommand:
    mission_id: str
    completed_at: Optional[str] = None

def update_mission(command: UpdateMissionCommand) -> Optional[Dict[str, Any]]:
    """미션 업데이트 (workflow에서 사용)"""
    update_data = {}

    if command.completed_at is not None:
        update_data["completed_at"] = command.completed_at

    mission = mission_repo.update_mission(command.mission_id, **update_data)
    if not mission:
        return None

    return {
        "id": mission["id"],
        "template_id": mission["template_id"],
        "completed_at": mission.get("completed_at"),
        "created_at": mission.get("created_at"),
        "updated_at": mission.get("updated_at")
    }

# 미션 삭제
@dataclass
class DeleteMissionCommand:
    mission_id: str

def remove_mission(command: DeleteMissionCommand) -> bool:
    """미션 삭제"""
    return mission_repo.delete_mission(command.mission_id)