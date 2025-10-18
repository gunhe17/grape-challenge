from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi import Request

from grapechallenge.domain.user import RepoUser
from grapechallenge.usecase.common.models import UsecaseOutput


class LoginUserInput(BaseModel):
    cell: str
    name: str


async def login_user(session: AsyncSession, request: Request, input: LoginUserInput) -> UsecaseOutput:

    # 입력 값 검증
    if not input.cell or not input.name:
        return UsecaseOutput(
            content={
                "message": "셀과 이름을 모두 입력해주세요."
            },
            code=400
        )

    # 사용자 조회
    login_result = await RepoUser.get_by_cell_and_name(
        session=session,
        cell=input.cell,
        name=input.name
    )

    if not login_result:
        return UsecaseOutput(
            content={
                "message": "등록되지 않은 사용자입니다. 셀과 이름을 확인해주세요."
            },
            code=404
        )

    user = login_result[0]

    return UsecaseOutput(
        content={
            "user_id": user.id,
            "message": "로그인 성공"
        },
        code=200
    )