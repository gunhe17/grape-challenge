from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, date
from repositories import mission, session, fruit
from usecases.mission import CreateMissionCommand, UpdateMissionCommand, create_mission, update_mission
from usecases.session import UpdateSessionCommand, update_session_on_mission_complete
from usecases.fruit import CreateFruitCommand, UpdateFruitStatusCommand, create_fruit, change_fruit_status
import random

# Mission 완료 Workflow (Atomic Transaction)
@dataclass
class CompleteMissionWorkflowCommand:
    user_id: str
    mission_template_id: str

def complete_mission_workflow(command: CompleteMissionWorkflowCommand) -> Dict[str, Any]:
    """Mission 완료 Workflow (Atomic Transaction) - DOCS.MD 설계를 정확히 구현"""

    # 1. 하루 1회 제한 체크 (오늘 날짜로 completed_at이 있는 mission 확인)
    today = date.today().isoformat()
    all_missions = mission.get_all_missions()

    # 오늘 완료된 mission이 있는지 확인 (completed_at 기준)
    today_completed = any(
        m.get('completed_at') and str(m.get('completed_at', '')).startswith(today)
        for m in all_missions
    )

    if today_completed:
        raise ValueError("하루 1회 미션 완료 제한에 걸렸습니다.")

    # 2. Mission 생성 (completed_at = now)
    create_cmd = CreateMissionCommand(template_id=command.mission_template_id)
    new_mission = create_mission(create_cmd)

    update_cmd = UpdateMissionCommand(
        mission_id=new_mission['id'],
        completed_at=datetime.now().isoformat()
    )
    updated_mission = update_mission(update_cmd)
    if not updated_mission:
        raise ValueError("미션 업데이트에 실패했습니다.")
    new_mission = updated_mission

    # 3. 현재 in-progress Session 조회
    current_session = session.get_session_by_user_and_status(command.user_id, "in progress")

    # Session이 없으면 새로 생성
    if not current_session:
        current_session = session.create_session(command.user_id)

    # current_session이 None일 수 없도록 보장
    if not current_session:
        raise ValueError("세션 생성에 실패했습니다.")

    # 4. Session의 mission_ids에 추가
    mission_ids = current_session.get('mission_ids', [])
    mission_ids.append(new_mission['id'])

    # 5. Session에 첫 mission인 경우: Fruit 생성 및 할당
    current_fruit = None
    if len(mission_ids) == 1:  # 첫 번째 mission
        # 랜덤 템플릿 선택
        fruit_templates = fruit.get_all_fruit_templates()
        if fruit_templates:
            random_template = random.choice(fruit_templates)
            fruit_cmd = CreateFruitCommand(template_id=random_template['id'], status='first')
            current_fruit = create_fruit(fruit_cmd)

            # Session의 fruit_id 업데이트
            session_update_cmd = UpdateSessionCommand(
                session_id=current_session['id'],
                fruit_id=current_fruit['id'],
                mission_ids=mission_ids
            )
            current_session = update_session_on_mission_complete(session_update_cmd)
        else:
            session_update_cmd = UpdateSessionCommand(
                session_id=current_session['id'],
                mission_ids=mission_ids
            )
            current_session = update_session_on_mission_complete(session_update_cmd)
    else:
        # 6. 기존 Fruit이 있는 경우 status 업데이트
        if current_session.get('fruit_id'):
            fruit_id = current_session.get('fruit_id')
            if fruit_id:
                current_fruit = fruit.get_fruit_by_id(fruit_id)
            if current_fruit:
                # mission_ids 개수에 따른 status 매핑
                status_map = {
                    1: 'first', 2: 'second', 3: 'third', 4: 'fourth',
                    5: 'fifth', 6: 'sixth', 7: 'seventh'
                }
                new_status = status_map.get(len(mission_ids), 'seventh')
                fruit_status_cmd = UpdateFruitStatusCommand(
                    fruit_id=current_fruit['id'],
                    status=new_status
                )
                current_fruit = change_fruit_status(fruit_status_cmd)

        # Session 업데이트
        session_update_cmd = UpdateSessionCommand(
            session_id=current_session['id'],
            mission_ids=mission_ids
        )
        current_session = update_session_on_mission_complete(session_update_cmd)

    # 7. mission_ids.length == 7인 경우: Session 완료 + 새 Session 생성
    if len(mission_ids) == 7:
        # 현재 Session status = 'completed'
        # current_session이 None이 아님을 보장
        if not current_session:
            raise ValueError("세션 정보를 찾을 수 없습니다.")

        complete_session_cmd = UpdateSessionCommand(
            session_id=current_session['id'],
            status='completed'
        )
        updated_session = update_session_on_mission_complete(complete_session_cmd)
        if updated_session:
            current_session = updated_session

        # 새 Session 생성 (fruit_id = null)
        new_session = session.create_session(command.user_id)

        return {
            "mission": new_mission,
            "session": current_session,
            "fruit": current_fruit,
            "new_session": new_session
        }

    # 성공 응답
    return {
        "mission": new_mission,
        "session": current_session,
        "fruit": current_fruit
    }

# 오늘의 Mission Template (랜덤 선택)
@dataclass
class GetRandomMissionTemplateQuery:
    pass

def get_random_mission_template(_query: GetRandomMissionTemplateQuery) -> Optional[Dict[str, Any]]:
    """오늘의 Mission Template (랜덤 선택)"""
    templates = mission.get_all_mission_templates()
    if not templates:
        return None

    selected_template = random.choice(templates)
    return {
        "id": selected_template["id"],
        "name": selected_template["name"],
        "type": selected_template["type"],
        "content": selected_template["content"],
        "created_at": selected_template.get("created_at"),
        "updated_at": selected_template.get("updated_at")
    }