import random
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.fruit import RepoFruit, Fruit, Status
from grapechallenge.domain.fruit_template import RepoFruitTemplate
from grapechallenge.domain.mission_template import RepoMissionTemplate
from grapechallenge.domain.mission import RepoMission
from grapechallenge.usecase.common.models import UsecaseOutput


class GetIsInProgressedFruitInput(BaseModel):
    pass


async def get_is_in_progressed_fruit(session: AsyncSession, request: Request, input: GetIsInProgressedFruitInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # found fruit
    found = await RepoFruit.get_is_in_progressed_by_user_id(
        session=session,
        user_id=user_id
    )

    if not found:
        return UsecaseOutput(
            content={
                "fruit": None,
                "missions": []
            },
            code=200
        )

    # Get mission templates
    mission_templates = await RepoMissionTemplate.get_all(session=session)

    # Build missions list with can_complete flag
    missions = []
    if mission_templates:
        for template in mission_templates:
            # Check if user has created a mission with this template today
            has_completed_today = await RepoMission.has_today_mission_with_template(
                session=session,
                user_id=user_id,
                template_id=template.id
            )

            missions.append({
                "template_id": template.id,
                "name": template.mission_template.name.to_str(),
                "content": template.mission_template.content.to_str(),
                "type": template.mission_template.type.to_str(),
                "can_complete": not has_completed_today
            })

    return UsecaseOutput(
        content={
            "fruit": {
                "fruit_id": found.get("fruit_id", None),
                "status": found.get("status", None),
                "name": found.get("name", None),
                "type": found.get("type", None),
                "first_status": found.get("first_status", None),
                "second_status": found.get("second_status", None),
                "third_status": found.get("third_status", None),
                "fourth_status": found.get("fourth_status", None),
                "fifth_status": found.get("fifth_status", None),
                "sixth_status": found.get("sixth_status", None),
                "seventh_status": found.get("seventh_status", None),
                "created_at": found.get("created_at").isoformat() if found.get("created_at") else None,
                "updated_at": found.get("updated_at").isoformat() if found.get("updated_at") else None,
            },
            "missions": missions
        },
        code=200
    )