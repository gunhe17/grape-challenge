from fastapi import Request, Depends
from fastapi.responses import JSONResponse

from grapechallenge.database.database import transactional_session_helper
from grapechallenge.usecase import (
    # command
    CreateFruitInput, create_fruit,
    # query
    GetIsInProgressedFruitInput, get_is_in_progressed_fruit,
    GetIsMineFruitsInput, get_is_mine_fruits,
)


# #
# Command

async def post_fruit(request: Request, input: CreateFruitInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await create_fruit(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


# #
# Query

async def get_mine_fruits(request: Request, input: GetIsMineFruitsInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_is_mine_fruits(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def get_in_progressed_fruit(request: Request, input: GetIsInProgressedFruitInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_is_in_progressed_fruit(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)