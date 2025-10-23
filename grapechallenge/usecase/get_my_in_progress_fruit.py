from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.fruit import RepoFruit
from grapechallenge.domain.mission_template import RepoMissionTemplate
from grapechallenge.domain.mission import RepoMission
from grapechallenge.usecase.common.models import UsecaseOutput
from grapechallenge.usecase.common.kst import kst


class GetMyInProgressFruitInput(BaseModel):
    pass

async def get_my_in_progress_fruit(session: AsyncSession, request: Request, input: GetMyInProgressFruitInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # found fruit
    found = await RepoFruit.get_my_in_progress(
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

    # get mission templates
    mission_templates = await RepoMissionTemplate.get_all(session=session)

    missions = []
    if mission_templates:
        for template in mission_templates:
            is_completed_today = await RepoMission.is_template_completed_today(
                session=session,
                user_id=user_id,
                template_id=template.id
            )
            can_complete = not is_completed_today
            missions.append((template, can_complete))

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
                "created_at": kst(found.get("created_at")), # type:ignore
                "updated_at": kst(found.get("updated_at")), # type:ignore
            },
            "missions": [
                {
                    "template_id": template.id,
                    "name": template.mission_template.name.to_str(),
                    "content": template.mission_template.content.to_str(),
                    "type": template.mission_template.type.to_str(),
                    "can_complete": can_complete
                }
                for template, can_complete in missions
            ]
        },
        code=200
    )
