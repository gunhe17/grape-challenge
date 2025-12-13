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
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if request is None:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if request is None:
                raise ValueError("Request object not found in function arguments")

            user_id = request.cookies.get("user_id")
            if not user_id:
                return RedirectResponse(url=redirect_if_fail, status_code=303)

            return await func(*args, **kwargs)

        return wrapper
    return decorator

def get_current_user(request: Request) -> dict | None:
    user_id = request.cookies.get("user_id")
    user_cell = request.cookies.get("user_cell")
    user_name = request.cookies.get("user_name")

    if user_id:
        return {
            "user_id": user_id,
            "user_cell": (
                unquote(user_cell) if user_cell else ""
            ),
            "user_name": (
                unquote(user_name) if user_name else ""
            )
        }

    return None


# #
# Template endpoints

async def login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("login.html", {
        "request": request
    })


async def christmas_login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("login_christmas.html", {
        "request": request
    })

@require_auth(redirect_if_fail="/christmas/login")
async def christmas_home_page(request: Request) -> HTMLResponse:
    user = get_current_user(request)
    app_env = get_app_env()
    return templates.TemplateResponse("home_christmas.html", {
        "request": request,
        "user": user,
        "app_env": app_env
    })

@require_auth(redirect_if_fail="/christmas/login")
async def christmas_diary_page(request: Request) -> HTMLResponse:
    user = get_current_user(request)
    return templates.TemplateResponse("diary_christmas.html", {
        "request": request,
        "user": user
    })

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


@require_auth()
async def report_page(request: Request) -> HTMLResponse:
    user = get_current_user(request)
    return templates.TemplateResponse("report.html", {
        "request": request,
        "user": user
    })

# admin
@require_auth()
async def admin_page(request: Request) -> HTMLResponse:
    user = get_current_user(request)
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "user": user
    })