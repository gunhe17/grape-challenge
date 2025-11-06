from urllib.parse import quote
from fastapi import Request, Depends
from fastapi.responses import JSONResponse

from grapechallenge.database.database import transactional_session_helper
from grapechallenge.usecase import (
    # command
    CreateUserInput, create_user,
    CreateUsersInput, create_users,
    LoginUserInput, login_user,
    LogoutUserInput, logout_user,
    # query
    GetCountAboutEveryUserInput, get_count_about_every_user,
    GetEveryCellInput, get_every_cell,
)


# #
# Command

async def post_user(request: Request, input: CreateUserInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await create_user(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def post_users(request: Request, input: CreateUsersInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await create_users(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def post_login(request: Request, input: LoginUserInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await login_user(session=session, request=request, input=input)

    response = JSONResponse(content=res.content, status_code=res.code)

    # 로그인 성공 시 쿠키 설정
    if res.code == 200 and res.content.get("user_id"):
        response.set_cookie(key="user_id", value=str(res.content["user_id"]), httponly=True, path="/", max_age=30*24*60*60)
        response.set_cookie(key="user_cell", value=quote(input.cell), httponly=False, path="/", max_age=30*24*60*60)
        response.set_cookie(key="user_name", value=quote(input.name), httponly=False, path="/", max_age=30*24*60*60)

    return response


async def post_logout(request: Request, input: LogoutUserInput) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await logout_user(session=session, request=request, input=input)

    response = JSONResponse(content=res.content, status_code=res.code)

    # 쿠키 삭제 (max_age=0으로 설정하여 즉시 만료)
    response.delete_cookie(key="user_id", path="/")
    response.delete_cookie(key="user_cell", path="/")
    response.delete_cookie(key="user_name", path="/")

    return response


# #
# Query

async def get_cells(request: Request, input: GetEveryCellInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_every_cell(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)


async def get_user_count(request: Request, input: GetCountAboutEveryUserInput = Depends()) -> JSONResponse:
    async with transactional_session_helper() as session:
        res = await get_count_about_every_user(session=session, request=request, input=input)

    return JSONResponse(content=res.content, status_code=res.code)