from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.usecase.common.models import UsecaseOutput


class LogoutUserInput(BaseModel):
    pass

async def logout_user(session: AsyncSession, request: Request, input: LogoutUserInput) -> UsecaseOutput:
    return UsecaseOutput(
        content={
            "message": "로그아웃 성공"
        },
        code=200
    )