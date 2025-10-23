from functools import wraps
from urllib.parse import unquote
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from grapechallenge.config import get_app_env

# Setup Jinja2 templates
BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "template"))


# #
# Auth helpers

def require_auth(redirect_if_fail: str = "/login"):
    """
    로그인이 필요한 페이지에 사용하는 데코레이터
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # request 객체 찾기
            request = kwargs.get("request")
            if request is None:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if request is None:
                raise ValueError("Request object not found in function arguments")

            # 쿠키에서 user_id 확인
            user_id = request.cookies.get("user_id")

            # 로그인되지 않은 경우 로그인 페이지로 리다이렉트
            if not user_id:
                return RedirectResponse(url=redirect_if_fail, status_code=303)

            # 로그인된 경우 원래 함수 실행
            return await func(*args, **kwargs)

        return wrapper
    return decorator


def get_current_user(request: Request) -> dict:
    """
    현재 로그인한 사용자 정보를 가져옵니다.
    """
    user_id = request.cookies.get("user_id")
    user_cell = request.cookies.get("user_cell")
    user_name = request.cookies.get("user_name")

    if user_id:
        return {
            "user_id": user_id,
            "user_cell": unquote(user_cell) if user_cell else "",
            "user_name": unquote(user_name) if user_name else ""
        }

    return None


# #
# Template endpoints

@require_auth()
async def home_page(request: Request) -> HTMLResponse:
    user = get_current_user(request)
    app_env = get_app_env()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "user": user,
        "app_env": app_env
    })


@require_auth()
async def grove_page(request: Request) -> HTMLResponse:
    user = get_current_user(request)
    return templates.TemplateResponse("grove.html", {
        "request": request,
        "user": user
    })


@require_auth()
async def diary_page(request: Request) -> HTMLResponse:
    user = get_current_user(request)
    return templates.TemplateResponse("diary.html", {
        "request": request,
        "user": user
    })


async def login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("login.html", {"request": request})