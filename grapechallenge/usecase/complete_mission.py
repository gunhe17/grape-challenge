from typing import Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.mission import RepoMission, Mission
from grapechallenge.domain.mission_template import RepoMissionTemplate
from grapechallenge.usecase.common.models import UsecaseOutput


class CompleteMissionInput(BaseModel):
    fruit_id: str
    name: str
    content: Optional[str] = None

async def complete_mission(session: AsyncSession, request: Request, input: CompleteMissionInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get templates
    found_templates = await RepoMissionTemplate.get_by_name(session=session, name=input.name)
    if not found_templates:
        return UsecaseOutput(
            content={
                "message": "No mission templates available"
            },
            code=404
        )

    # create mission
    created = await RepoMission.create(
        session=session,
        mission=Mission.new(
            user_id=user_id,
            fruit_id=input.fruit_id,
            template_id=(
                found_templates.id
            ),
            content=input.content or "",
        )
    )

    # update fruit
    from grapechallenge.domain.fruit.repo_fruit import RepoFruit
    found_fruit = await RepoFruit.get_by_id(session=session, id=input.fruit_id)
    if not found_fruit:
        return UsecaseOutput(
            content={
                "message": "No matched fruits found"
            },
            code=404
        )
    
    updated_fruit = await RepoFruit.update(
        session=session,
        fruit=(
            found_fruit.fruit.next_status()
        ),
        id=found_fruit.id
    )
    
    return UsecaseOutput(
        content={
            **created.summary(),
        },
        code=201
    )