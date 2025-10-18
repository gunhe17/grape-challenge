from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.usecase.common.models import UsecaseOutput


class LogoutUserInput(BaseModel):
    pass


async def logout_user(session: AsyncSession, request: Request, input: LogoutUserInput) -> UsecaseOutput:
    # 로그아웃은 단순히 성공 응답을 반환
    # 실제 쿠키 삭제는 endpoint에서 처리
    return UsecaseOutput(
        content={
            "message": "로그아웃 성공"
        },
        code=200
    )
