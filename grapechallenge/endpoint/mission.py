from fastapi import Request
from fastapi.responses import JSONResponse

from grapechallenge.database.database import transactional_session_helper
from grapechallenge.usecase import (
    # command
    CompleteMissionInput, complete_mission,
    CompleteTestMissionInput, complete_test_mission,
)


# #
# Command

async def post_mission(request: Request, input: CompleteMissionInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await complete_mission(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def post_test_mission(request: Request, input: CompleteTestMissionInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await complete_test_mission(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)