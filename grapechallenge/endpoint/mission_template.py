from fastapi import Request, Depends
from fastapi.responses import JSONResponse

from grapechallenge.database.database import transactional_session_helper
from grapechallenge.usecase import (
    # command
    UpdateMissionTemplateInput, update_mission_template,
    # query
    GetMissionTemplatesInput, get_mission_templates,
)


# #
# Command

async def patch_mission_template(request: Request, input: UpdateMissionTemplateInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await update_mission_template(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


# #
# Query

async def get_every_mission_template(request: Request, input: GetMissionTemplatesInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_mission_templates(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)
