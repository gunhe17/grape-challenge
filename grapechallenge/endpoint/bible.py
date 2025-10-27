from fastapi import Request, Depends
from fastapi.responses import JSONResponse

from grapechallenge.database.database import transactional_session_helper
from grapechallenge.usecase import (
    # command
    CreateBibleVerseInput, create_bible_verse,
    CreateBibleVersesInput, create_bible_verses,
    # query
    GetTodayBibleVerseInput, get_today_bible_verse,
)


# #
# Command

async def post_bible_verse(request: Request, input: CreateBibleVerseInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await create_bible_verse(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def post_bible_verses(request: Request, input: CreateBibleVersesInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await create_bible_verses(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


# #
# Query

async def get_today_verse(request: Request, input: GetTodayBibleVerseInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_today_bible_verse(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)
