from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.mission_template import RepoMissionTemplate
from grapechallenge.domain.mission import RepoMission
from grapechallenge.usecase.common.models import UsecaseOutput


async def get_event_missions_in_progress(session: AsyncSession, request: Request) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get EVENT mission templates
    mission_templates = await RepoMissionTemplate.get_all(
        session=session,
        type_filter="EVENT"
    )

    if not mission_templates:
        return UsecaseOutput(
            content={
                "missions": []
            },
            code=200
        )

    missions = []
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
