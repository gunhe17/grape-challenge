from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.user import RepoUser
from grapechallenge.usecase.common.models import UsecaseOutput


class GetCountAboutEveryUserInput(BaseModel):
    pass

async def get_count_about_every_user(session: AsyncSession, request: Request, input: GetCountAboutEveryUserInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get count
    count = await RepoUser.count_all(session=session)

    return UsecaseOutput(
        content={
            "count": count
        },
        code=200
    )
