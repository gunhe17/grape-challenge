from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.fruit import RepoFruit, Status
from grapechallenge.usecase.common.models import UsecaseOutput


class HarvestFruitInput(BaseModel):
    fruit_id: str

async def harvest_fruit(session: AsyncSession, request: Request, input: HarvestFruitInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # found fruit
    found_fruit = await RepoFruit.get_by_id(session=session, id=input.fruit_id)
    if not found_fruit:
        return UsecaseOutput(
            content={
                "message": "No matched fruits found"
            },
            code=404
        )

    # TODO
    # check if fruit belongs to user
    if found_fruit.fruit.user_id != user_id:
        return UsecaseOutput(
            content={
                "message": "Unauthorized"
            },
            code=403
        )

    # check if fruit is in SEVENTH_STATUS
    if found_fruit.fruit.status.to_str() != "SEVENTH_STATUS":
        return UsecaseOutput(
            content={
                "message": "Fruit is not ready for harvest"
            },
            code=400
        )

    # update fruit to COMPLETED
    updated_fruit = await RepoFruit.update(
        session=session,
        fruit=found_fruit.fruit.__class__.new(
            user_id=found_fruit.fruit.user_id,
            template_id=found_fruit.fruit.template_id,
            status=Status.from_str("COMPLETED")
        ),
        id=found_fruit.id
    )

    return UsecaseOutput(
        content={
            **updated_fruit.summary()
        },
        code=200
    )
