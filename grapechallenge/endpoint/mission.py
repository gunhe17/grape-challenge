from fastapi import Request, Depends
from fastapi.responses import JSONResponse, Response

from grapechallenge.database.database import transactional_session_helper
from grapechallenge.usecase import (
    # command
    CompleteMissionInput, complete_mission,
    CompleteTestMissionInput, complete_test_mission,
    # query
    GetMissionsByNameInput, get_missions_by_name,
    WriteDailyMissionReportInput, write_daily_mission_report,
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


# #
# Query

async def get_missions(request: Request, input: GetMissionsByNameInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_missions_by_name(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def get_daily_mission_report(request: Request, input: WriteDailyMissionReportInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await write_daily_mission_report(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)

