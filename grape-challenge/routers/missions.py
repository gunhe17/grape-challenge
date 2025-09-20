from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from ..repositories.mission_repository import MissionRepository, MissionTemplateRepository
from ..routers.auth import get_current_user, require_admin
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["missions"])
mission_repo = MissionRepository()
mission_template_repo = MissionTemplateRepository()

class MissionCreate(BaseModel):
    template_id: int
    user_id: int
    status: str = 'pending'

# Mission endpoints
@router.post("/missions")
def create_mission(
    mission: MissionCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    if mission.user_id != current_user["id"] and current_user["role"] != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    return mission_repo.create_mission(mission.template_id, mission.user_id, mission.status)

@router.get("/missions/{mission_id}")
def get_mission(
    mission_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    mission = mission_repo.get_by_id(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    if mission.get("user_id") != current_user["id"] and current_user["role"] != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return mission

@router.get("/missions")
def get_all_missions(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    if current_user["role"] == 'admin':
        return mission_template_repo.get_all_templates()  # Return all missions for admin
    else:
        return mission_repo.get_by_user_id(current_user["id"])

class MissionUpdate(BaseModel):
    status: Optional[str] = None
    template_id: Optional[int] = None

@router.put("/missions/{mission_id}")
def update_mission(
    mission_id: int,
    mission_update: MissionUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    mission = mission_repo.get_by_id(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    if mission.get("user_id") != current_user["id"] and current_user["role"] != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = mission_update.dict(exclude_unset=True)
    updated_mission = mission_repo.update(mission_id, **update_data)
    return updated_mission

@router.patch("/missions/{mission_id}/complete")
def complete_mission(
    mission_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    mission = mission_repo.get_by_id(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    if mission.get("user_id") != current_user["id"] and current_user["role"] != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_mission = mission_repo.complete_mission(mission_id)
    if not updated_mission or updated_mission.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Failed to complete mission")
    
    return {"success": True, "message": "Mission completed successfully", "mission": updated_mission}

@router.delete("/missions/{mission_id}")
def delete_mission(
    mission_id: int,
    current_user: Dict[str, Any] = Depends(require_admin)
):
    if not mission_repo.delete(mission_id):
        raise HTTPException(status_code=404, detail="Mission not found")
    return {"message": "Mission deleted successfully"}

class MissionTemplateCreate(BaseModel):
    name: str
    type: str = 'normal'
    content: str = ''

class MissionTemplateUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    content: Optional[str] = None

# Mission Template endpoints
@router.post("/mission-templates")
def create_mission_template(
    template: MissionTemplateCreate,
    current_user: Dict[str, Any] = Depends(require_admin)
):
    return mission_template_repo.create_template(
        name=template.name,
        type=template.type,
        content=template.content
    )

@router.get("/mission-templates")
def get_all_mission_templates():
    return mission_template_repo.get_all_templates()

@router.get("/mission-templates/{template_id}")
def get_mission_template(template_id: int):
    template = mission_template_repo.get_by_id(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Mission template not found")
    return template

@router.put("/mission-templates/{template_id}")
def update_mission_template(
    template_id: int,
    template_update: MissionTemplateUpdate,
    current_user: Dict[str, Any] = Depends(require_admin)
):
    update_data = template_update.dict(exclude_unset=True)
    updated_template = mission_template_repo.update_template(template_id, **update_data)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Mission template not found")
    return updated_template

@router.patch("/mission-templates/{template_id}")
def patch_mission_template(
    template_id: int,
    template_update: MissionTemplateUpdate,
    current_user: Dict[str, Any] = Depends(require_admin)
):
    update_data = template_update.dict(exclude_unset=True)
    updated_template = mission_template_repo.update_template(template_id, **update_data)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Mission template not found")
    return updated_template

@router.delete("/mission-templates/{template_id}")
def delete_mission_template(
    template_id: int,
    current_user: Dict[str, Any] = Depends(require_admin)
):
    if not mission_template_repo.delete(template_id):
        raise HTTPException(status_code=404, detail="Mission template not found")
    return {"message": "Mission template deleted successfully"}