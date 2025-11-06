from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.mission_template import RepoMissionTemplate
from grapechallenge.usecase.common.models import UsecaseOutput
from grapechallenge.usecase.common.kst import kst


class GetMissionTemplatesInput(BaseModel):
    pass

async def get_mission_templates(session: AsyncSession, request: Request, input: GetMissionTemplatesInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get all mission templates
    founds = await RepoMissionTemplate.get_all(session=session)

    if not founds:
        return UsecaseOutput(
            content={
                "mission_templates": [],
                "count": 0
            },
            code=200
        )

    return UsecaseOutput(
        content={
            "mission_templates": [
                {
                    "id": found.id,
                    "name": found.mission_template.name.to_str(),
                    "content": found.mission_template.content.to_str(),
                    "type": found.mission_template.type.to_str(),
                    "created_at": kst(found.created_at),
                    "updated_at": kst(found.updated_at),
                }
                for found in founds
            ],
            "count": len(founds)
        },
        code=200
    )
