import random
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.fruit import RepoFruit, Fruit, Status
from grapechallenge.domain.fruit_template import RepoFruitTemplate
from grapechallenge.usecase.common.models import UsecaseOutput


class CreateFruitInput(BaseModel):
    pass

async def create_fruit(session: AsyncSession, request: Request, input: CreateFruitInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=404)
    
    # get templates
    found_templates = await RepoFruitTemplate.get_all(session=session)
    if not found_templates:
        return UsecaseOutput(
            content={
                "message": "No fruit templates available"
            },
            code=404
        )

    # create fruit
    created = await RepoFruit.create(
        session=session,
        fruit=Fruit.new(
            user_id=user_id,
            template_id=(
                random.choice(found_templates).id # *random choose
            ),
            status=Status.from_str("FIRST_STATUS"),
        )
    )

    return UsecaseOutput(
        content={
            **created.summary()
        },
        code=201
    )