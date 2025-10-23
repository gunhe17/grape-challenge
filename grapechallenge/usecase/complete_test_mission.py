from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.config import get_app_env
from grapechallenge.domain.fruit import RepoFruit
from grapechallenge.usecase.common.models import UsecaseOutput


class CompleteTestMissionInput(BaseModel):
    fruit_id: str

async def complete_test_mission(session: AsyncSession, request: Request, input: CompleteTestMissionInput) -> UsecaseOutput:
    # check env
    app_env = get_app_env()
    if app_env != "dev":
        return UsecaseOutput(
            content={"message": "Test mission is only available in dev environment"},
            code=403
        )

    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get fruit
    found_fruit = await RepoFruit.get_by_id(session=session, id=input.fruit_id)
    if not found_fruit:
        return UsecaseOutput(
            content={
                "message": "No matched fruits found"
            },
            code=404
        )

    # verify ownership
    if found_fruit.fruit.user_id != user_id:
        return UsecaseOutput(
            content={
                "message": "Unauthorized access to fruit"
            },
            code=403
        )

    # update fruit
    updated_fruit = await RepoFruit.update(
        session=session,
        fruit=(
            found_fruit.fruit.next_status()
        ),
        id=found_fruit.id
    )

    return UsecaseOutput(
        content={
            "fruit_id": updated_fruit.id,
            "status": updated_fruit.fruit.status.to_str(),
            "test_mode": True
        },
        code=200
    )
