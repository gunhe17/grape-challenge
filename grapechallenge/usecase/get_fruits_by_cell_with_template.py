from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.fruit import RepoFruit
from grapechallenge.usecase.common.models import UsecaseOutput


class GetFruitsByCellWithTemplateInput(BaseModel):
    cell: str

async def get_fruits_by_cell_with_template(session: AsyncSession, request: Request, input: GetFruitsByCellWithTemplateInput) -> UsecaseOutput:
    
    # get fruits by cell
    founds = await RepoFruit.get_by_cell_with_template(
        session=session,
        cell=input.cell
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
                    "fruit_id": found.get("fruit_id", None),
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