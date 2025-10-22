from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.user import RepoUser
from grapechallenge.usecase.common.models import UsecaseOutput


class GetEveryCellInput(BaseModel):
    pass

async def get_every_cell(session: AsyncSession, request: Request, input: GetEveryCellInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get all cells
    cells = await RepoUser.get_all_cells(session=session)

    if not cells:
        return UsecaseOutput(
            content={
                "cells": [],
                "count": 0
            },
            code=200
        )

    return UsecaseOutput(
        content={
            "cells": cells,
            "count": len(cells)
        },
        code=200
    )
