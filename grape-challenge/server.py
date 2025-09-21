"""
Grape Challenge API Server - Essential Features Only
"""
from fastapi import FastAPI, HTTPException
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

app = FastAPI(title="Grape Challenge API")

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
# Core APIs
# =============================================================================

@app.post("/user")
def create_user_api(request: CreateUserRequest):
    return api_create_user(request.name, request.cell, request.role)

@app.post("/login")
def login_api(request: LoginRequest):
    result = api_login(request.name, request.cell)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return result

@app.post("/session")
def start_session_api(user_id: str):
    return api_start_session(user_id)

@app.get("/session/user/{user_id}/in-progress")
def get_in_progress_session_api(user_id: str):
    result = api_get_in_progress_session(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="No active session")
    return result

@app.post("/mission/complete")
def complete_mission_api(request: CompleteMissionRequest):
    try:
        return api_complete_mission(request.user_id, request.mission_template_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/mission-templates")
def get_mission_templates_api():
    return api_get_mission_templates()

@app.get("/mission-template/random")
def get_random_mission_template_api():
    result = api_get_random_mission_template()
    if not result:
        raise HTTPException(status_code=404, detail="No templates available")
    return result

@app.post("/mission-template")
def create_mission_template_api(request: CreateMissionTemplateRequest):
    return api_create_mission_template(request.name, request.type, request.content)

@app.get("/fruit-templates")
def get_fruit_templates_api():
    return api_get_fruit_templates()

@app.post("/fruit-template")
def create_fruit_template_api(request: CreateFruitTemplateRequest):
    return api_create_fruit_template(request.name, request.type, request.status_images)

@app.get("/admin/statistics")
def get_admin_statistics_api():
    return api_get_admin_statistics()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)