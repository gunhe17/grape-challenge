from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.fruit_template import RepoFruitTemplate
from grapechallenge.usecase.common.models import UsecaseOutput


class GetFruitTemplateByNameInput(BaseModel):
    name: str

async def get_fruit_template_by_name(session: AsyncSession, request: Request, input: GetFruitTemplateByNameInput) -> UsecaseOutput:

    # get fruit template
    founds = await RepoFruitTemplate.get_by_name(
        session=session,
        name=input.name
    )

    if not founds:
        return UsecaseOutput(
            content={
                "message": "fruit template not found"
            },
            code=404
        )

    return UsecaseOutput(
        content={
            "fruit_templates": [
                {
                    **found.summary()
                }
                for found in founds
            ]
        },
        code=200
    )