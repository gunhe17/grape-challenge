from typing import Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.mission_template import (
    RepoMissionTemplate,
    MissionTemplate,
    Name,
    Content,
    Type,
)
from grapechallenge.usecase.common.models import UsecaseOutput


class UpdateMissionTemplateInput(BaseModel):
    id: str
    name: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None

async def update_mission_template(session: AsyncSession, request: Request, input: UpdateMissionTemplateInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get existing mission template
    found = await RepoMissionTemplate.get_by_id(session=session, id=input.id)
    if not found:
        return UsecaseOutput(
            content={
                "message": "Mission template not found"
            },
            code=404
        )

    # update mission template
    updated = await RepoMissionTemplate.update(
        session=session,
        mission_template=MissionTemplate.new(
            name=(
                Name.from_str(input.name) if input.name else found.mission_template.name
            ),
            content=(
                Content.from_str(input.content) if input.content else found.mission_template.content
            ),
            type=(
                Type.from_str(input.type) if input.type else found.mission_template.type
            ),
        ),
        id=input.id
    )

    return UsecaseOutput(
        content={
            **updated.summary(),
            "name": updated.mission_template.name.to_str(),
            "content": updated.mission_template.content.to_str(),
            "type": updated.mission_template.type.to_str(),
        },
        code=200
    )
