"""
Mission domain endpoint helpers
"""
from typing import Optional, Dict, Any, List
from usecases import mission, mission_workflow


def api_create_mission_template(name: str, type: str = 'normal', content: str = '') -> Dict[str, Any]:
    """미션 템플릿 생성 API (Admin)"""
    command = mission.CreateMissionTemplateCommand(name=name, type=type, content=content)
    return mission.create_mission_template_admin(command)


def api_get_mission_templates() -> List[Dict[str, Any]]:
    """미션 템플릿 목록 조회 API"""
    query = mission.GetAllMissionTemplatesQuery()
    return mission.get_mission_template_list(query)


def api_get_mission_template(template_id: str) -> Optional[Dict[str, Any]]:
    """미션 템플릿 조회 API"""
    query = mission.GetMissionTemplateQuery(template_id=template_id)
    return mission.get_mission_template_info(query)


def api_update_mission_template(template_id: str, name: Optional[str] = None,
                               type: Optional[str] = None,
                               content: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """템플릿 내용 수정 API (Admin)"""
    command = mission.UpdateMissionTemplateCommand(
        template_id=template_id,
        name=name,
        type=type,
        content=content
    )
    return mission.update_mission_template_admin(command)


def api_create_mission(template_id: str) -> Dict[str, Any]:
    """미션 생성 API"""
    command = mission.CreateMissionCommand(template_id=template_id)
    return mission.create_mission(command)


def api_get_mission(mission_id: str) -> Optional[Dict[str, Any]]:
    """미션 조회 API"""
    query = mission.GetMissionQuery(mission_id=mission_id)
    return mission.get_mission_info(query)


def api_delete_mission(mission_id: str) -> bool:
    """미션 삭제 API"""
    command = mission.DeleteMissionCommand(mission_id=mission_id)
    return mission.remove_mission(command)


def api_complete_mission(user_id: str, mission_template_id: str) -> Dict[str, Any]:
    """미션 완료 Workflow API (핵심 비즈니스 로직)"""
    command = mission_workflow.CompleteMissionWorkflowCommand(
        user_id=user_id,
        mission_template_id=mission_template_id
    )
    return mission_workflow.complete_mission_workflow(command)


def api_get_random_mission_template() -> Optional[Dict[str, Any]]:
    """오늘의 미션 템플릿 (랜덤 선택) API"""
    query = mission_workflow.GetRandomMissionTemplateQuery()
    return mission_workflow.get_random_mission_template(query)