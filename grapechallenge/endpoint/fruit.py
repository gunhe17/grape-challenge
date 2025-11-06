from fastapi import Request, Depends
from fastapi.responses import JSONResponse

from grapechallenge.database.database import transactional_session_helper
from grapechallenge.usecase import (
    # command
    CreateFruitInput, create_fruit,
    HarvestFruitInput, harvest_fruit,
    # query
    CountMyCompletedFruitsInput, count_my_completed_fruits as count_my_completed_fruits_usecase,
    GetCountAboutEveryFruitInput, get_count_about_every_fruit,
    GetFruitStatsByTemplateInput, get_fruit_stats_by_template as get_fruit_stats_by_template_usecase,
    GetFruitsByCellWithTemplateInput, get_fruits_by_cell_with_template as get_fruits_by_cell_with_template_usecase,
    GetMyFruitsInput, get_my_fruits as get_my_fruits_usecase,
    GetMyInProgressFruitInput, get_my_in_progress_fruit as get_my_in_progress_fruit_usecase,
)


# #
# Command

async def post_fruit(request: Request, input: CreateFruitInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await create_fruit(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def post_harvest_fruit(request: Request, input: HarvestFruitInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await harvest_fruit(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


# #
# Query

async def get_my_fruits(request: Request, input: GetMyFruitsInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_my_fruits_usecase(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def get_my_in_progress_fruit(request: Request, input: GetMyInProgressFruitInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_my_in_progress_fruit_usecase(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def count_my_completed_fruits(request: Request, input: CountMyCompletedFruitsInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await count_my_completed_fruits_usecase(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def get_fruits_by_cell_with_template(request: Request, input: GetFruitsByCellWithTemplateInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_fruits_by_cell_with_template_usecase(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def get_fruit_count(request: Request, input: GetCountAboutEveryFruitInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_count_about_every_fruit(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def get_fruit_stats_by_template(request: Request, input: GetFruitStatsByTemplateInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_fruit_stats_by_template_usecase(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)