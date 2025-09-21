"""
Grape Challenge Unified Server - API + Web Interface
"""
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional

from endpoints.user_endpoint import api_create_user, api_login
from endpoints.session_endpoint import api_start_session, api_get_in_progress_session
from endpoints.fruit_endpoint import api_get_fruit_templates, api_create_fruit_template
from endpoints.mission_endpoint import (
    api_complete_mission, api_get_mission_templates, api_get_random_mission_template,
    api_create_mission_template
)
from endpoints.admin_endpoint import api_get_admin_statistics
from endpoints.page_endpoint import (
    page_login, page_login_post, page_home, page_mission_complete,
    page_fruits, page_admin
)

app = FastAPI(title="Grape Challenge - Unified Application")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# =============================================================================
# Request Models
# =============================================================================

class CreateUserRequest(BaseModel):
    name: str
    cell: str
    role: str = 'user'

class LoginRequest(BaseModel):
    name: str
    cell: str

class CompleteMissionRequest(BaseModel):
    user_id: str
    mission_template_id: str

class CreateMissionTemplateRequest(BaseModel):
    name: str
    type: str = 'normal'
    content: str = ''

class CreateFruitTemplateRequest(BaseModel):
    name: str
    type: str = 'normal'
    status_images: Optional[dict] = None

# =============================================================================
# API Routes (with /api prefix)
# =============================================================================

@app.post("/api/user")
def create_user_api(request: CreateUserRequest):
    return api_create_user(request.name, request.cell, request.role)

@app.post("/api/login")
def login_api(request: LoginRequest):
    result = api_login(request.name, request.cell)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return result

@app.post("/api/session")
def start_session_api(user_id: str):
    return api_start_session(user_id)

@app.get("/api/session/user/{user_id}/in-progress")
def get_in_progress_session_api(user_id: str):
    result = api_get_in_progress_session(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="No active session")
    return result

@app.post("/api/mission/complete")
def complete_mission_api(request: CompleteMissionRequest):
    try:
        return api_complete_mission(request.user_id, request.mission_template_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/mission-templates")
def get_mission_templates_api():
    return api_get_mission_templates()

@app.get("/api/mission-template/random")
def get_random_mission_template_api():
    result = api_get_random_mission_template()
    if not result:
        raise HTTPException(status_code=404, detail="No templates available")
    return result

@app.post("/api/mission-template")
def create_mission_template_api(request: CreateMissionTemplateRequest):
    return api_create_mission_template(request.name, request.type, request.content)

@app.get("/api/fruit-templates")
def get_fruit_templates_api():
    return api_get_fruit_templates()

@app.post("/api/fruit-template")
def create_fruit_template_api(request: CreateFruitTemplateRequest):
    return api_create_fruit_template(request.name, request.type, request.status_images)

@app.get("/api/admin/statistics")
def get_admin_statistics_api():
    return api_get_admin_statistics()

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

# =============================================================================
# Web Interface Routes
# =============================================================================

@app.get("/")
async def root():
    return RedirectResponse(url="/login", status_code=302)

@app.get("/login")
async def login_page(request: Request):
    return page_login(request)

@app.post("/login")
async def login_post(request: Request, name: str = Form(...), cell: str = Form(...)):
    return page_login_post(request, name, cell)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response

@app.get("/home")
async def home_page(request: Request):
    return page_home(request)

@app.post("/mission/complete")
async def complete_mission(request: Request, mission_template_id: str = Form(...)):
    return page_mission_complete(request, mission_template_id)

@app.get("/fruits")
async def fruits_page(request: Request):
    return page_fruits(request)

@app.get("/admin")
async def admin_page(request: Request):
    return page_admin(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)