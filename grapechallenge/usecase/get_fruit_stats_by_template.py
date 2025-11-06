from fastapi import Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from grapechallenge.domain.fruit.repo_fruit import RepoFruit
from grapechallenge.usecase.common.models import UsecaseOutput


class GetFruitStatsByTemplateInput(BaseModel):
    pass


async def get_fruit_stats_by_template(
    session: AsyncSession,
    request: Request,
    input: GetFruitStatsByTemplateInput
) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    stats = await RepoFruit.get_stats_by_template(session=session)

    if not stats:
        return UsecaseOutput(content={"stats": []}, code=200)

    return UsecaseOutput(content={"stats": stats}, code=200)
