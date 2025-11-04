from typing import Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.mission import RepoMission
from grapechallenge.usecase.common.models import UsecaseOutput
from grapechallenge.usecase.common.kst import kst


class GetMissionsByNameInput(BaseModel):
    name: str
    date: Optional[str] = None

async def get_missions_by_name(session: AsyncSession, request: Request, input: GetMissionsByNameInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get missions
    founds = await RepoMission.get_by_template_name(
        session=session,
        name=input.name,
        date=input.date
    )

    if not founds:
        return UsecaseOutput(
            content={
                "missions": [],
                "count": 0
            },
            code=200
        )

    return UsecaseOutput(
        content={
            "missions": [
                {
                    "id": found.get("mission_id", None),
                    "name": found.get("template_name", None),
                    "content": found.get("mission_content", None),
                    "content_created_at": kst(found.get("mission_created_at")), # type:ignore
                    "user_id": found.get("user_id", None),
                    "user_cell": found.get("user_cell", None),
                    "user_name": found.get("user_name", None),
                    "interaction": found.get("mission_interaction", None),
                }
                for found in founds
            ],
            "count": len(founds),
            "user_id": user_id,
        },
        code=200
    )