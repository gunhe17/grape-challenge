from fastapi import Request, Depends
from fastapi.responses import JSONResponse

from grapechallenge.database.database import transactional_session_helper
from grapechallenge.usecase import (
    # query
    GetFruitTemplateByNameInput, get_fruit_template_by_name,
)


# #
# Query

async def get_fruit_template(request: Request, input: GetFruitTemplateByNameInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_fruit_template_by_name(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)
