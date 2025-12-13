from typing import Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.mission import RepoMission, Mission, Content
from grapechallenge.domain.mission_template import RepoMissionTemplate
from grapechallenge.usecase.common.models import UsecaseOutput


class CompleteEventMissionInput(BaseModel):
    name: str
    content: Optional[str] = None


async def complete_event_mission(session: AsyncSession, request: Request, input: CompleteEventMissionInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get EVENT template by name
    found_template = await RepoMissionTemplate.get_by_name(session=session, name=input.name)
    if not found_template:
        return UsecaseOutput(
            content={
                "message": "No mission template found"
            },
            code=404
        )

    # verify it's an EVENT type template
    if found_template.mission_template.type.to_str() != "EVENT":
        return UsecaseOutput(
            content={
                "message": "This is not an EVENT mission"
            },
            code=400
        )

    # check if already completed today
    is_completed_today = await RepoMission.is_template_completed_today(
        session=session,
        user_id=user_id,
        template_id=found_template.id
    )
    if is_completed_today:
        return UsecaseOutput(
            content={
                "message": "Mission already completed today"
            },
            code=400
        )

    # create mission (without fruit_id)
    created = await RepoMission.create(
        session=session,
        mission=Mission.new(
            user_id=user_id,
            fruit_id=None,
            template_id=found_template.id,
            content=(
                Content.from_str(input.content) if input.content else None
            ),
            interaction=None
        )
    )

    return UsecaseOutput(
        content={
            **created.summary(),
        },
        code=201
    )
