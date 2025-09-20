from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

# Templates 경로 설정
templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """로그인 페이지 (기본 페이지)"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_redirect(request: Request):
    """로그인 페이지"""
    return templates.TemplateResponse("login.html", {"request": request})