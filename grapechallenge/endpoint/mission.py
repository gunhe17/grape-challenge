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


async def get_daily_mission_report(request: Request) -> JSONResponse:
    """Generate and return daily mission report as JSON with base64 images"""
    import base64

    async with transactional_session_helper() as session:
        res = await write_daily_mission_report(
            session=session,
            request=request,
            input=WriteDailyMissionReportInput()
        )

        if res.code != 200:
            return JSONResponse(content=res.content, status_code=res.code)

        # Convert image bytes to base64 for JSON response
        image_bytes_list = res.content.get("image_bytes_list", [])
        if not image_bytes_list:
            return JSONResponse(content={"message": "No image generated"}, status_code=500)

        image_bytes_base64 = [base64.b64encode(img_bytes).decode('utf-8') for img_bytes in image_bytes_list]

        return JSONResponse(content={
            "image_bytes_list": image_bytes_base64,
            "page_count": res.content.get("page_count", 0),
            "count": res.content.get("count", 0),
            "message": res.content.get("message", "")
        }, status_code=200)

