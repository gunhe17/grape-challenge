from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.fruit import RepoFruit
from grapechallenge.usecase.common.models import UsecaseOutput


class GetMyFruitsInput(BaseModel):
    pass

async def get_my_fruits(session: AsyncSession, request: Request, input: GetMyFruitsInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get fruits
    founds = await RepoFruit.get_by_user_id_with_template(
        session=session,
        user_id=user_id
    )

    if not founds:
        return UsecaseOutput(
            content={
                "fruits": [],
                "count": 0
            },
            code=200
        )

    return UsecaseOutput(
        content={
            "fruits": [
                {
                    "fruit_id": found.get("get", None),
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
                    "created_at": found.get("created_at").isoformat() if found.get("created_at") else None, # type:ignore
                    "updated_at": found.get("updated_at").isoformat() if found.get("updated_at") else None, # type:ignore
                }
                for found in founds
            ],
            "count": len(founds)
        },
        code=200
    )