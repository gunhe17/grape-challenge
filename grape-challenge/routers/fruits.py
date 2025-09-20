from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from typing import Dict, Any
from ..repositories.fruit_repository import FruitRepository, FruitTemplateRepository
from ..routers.auth import get_current_user, require_admin
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["fruits"])
fruit_repo = FruitRepository()
fruit_template_repo = FruitTemplateRepository()

class FruitCreate(BaseModel):
    template_id: int
    status: str = '씨앗'

# Fruit endpoints
@router.post("/fruits")
def create_fruit(
    fruit: FruitCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    return fruit_repo.create_fruit(fruit.template_id, fruit.status)

@router.get("/fruits/{fruit_id}")
def get_fruit(
    fruit_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    fruit = fruit_repo.get_by_id(fruit_id)
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return fruit

class FruitUpdate(BaseModel):
    status: Optional[str] = None
    template_id: Optional[int] = None

@router.put("/fruits/{fruit_id}")
def update_fruit(
    fruit_id: int,
    fruit_update: FruitUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    update_data = fruit_update.dict(exclude_unset=True)
    updated_fruit = fruit_repo.update(fruit_id, **update_data)
    if not updated_fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return updated_fruit

class FruitStatusUpdate(BaseModel):
    status: str

@router.patch("/fruits/{fruit_id}/status")
def update_fruit_status(
    fruit_id: int,
    status_update: FruitStatusUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    updated_fruit = fruit_repo.update_status(fruit_id, status_update.status)
    if not updated_fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return updated_fruit

@router.delete("/fruits/{fruit_id}")
def delete_fruit(
    fruit_id: int,
    current_user: Dict[str, Any] = Depends(require_admin)
):
    if not fruit_repo.delete(fruit_id):
        raise HTTPException(status_code=404, detail="Fruit not found")
    return {"message": "Fruit deleted successfully"}

class FruitTemplateCreate(BaseModel):
    name: str
    type: str = 'normal'
    seed_image: Optional[str] = None
    sprout_image: Optional[str] = None
    tree_image: Optional[str] = None
    fruit_image: Optional[str] = None

# Fruit Template endpoints
@router.post("/fruit-templates")
def create_fruit_template(
    template: FruitTemplateCreate,
    current_user: Dict[str, Any] = Depends(require_admin)
):
    return fruit_template_repo.create_template(
        name=template.name,
        type=template.type,
        seed_image=template.seed_image,
        sprout_image=template.sprout_image,
        tree_image=template.tree_image,
        fruit_image=template.fruit_image
    )

@router.get("/fruit-templates")
def get_all_fruit_templates():
    return fruit_template_repo.get_all_templates()

@router.get("/fruit-templates/{template_id}")
def get_fruit_template(template_id: int):
    template = fruit_template_repo.get_by_id(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Fruit template not found")
    return template

class FruitTemplateUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    seed_image: Optional[str] = None
    sprout_image: Optional[str] = None
    tree_image: Optional[str] = None
    fruit_image: Optional[str] = None

@router.put("/fruit-templates/{template_id}")
def update_fruit_template(
    template_id: int,
    template_update: FruitTemplateUpdate,
    current_user: Dict[str, Any] = Depends(require_admin)
):
    update_data = template_update.dict(exclude_unset=True)
    updated_template = fruit_template_repo.update_template(template_id, **update_data)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Fruit template not found")
    return updated_template

@router.patch("/fruit-templates/{template_id}")
def patch_fruit_template(
    template_id: int,
    template_update: FruitTemplateUpdate,
    current_user: Dict[str, Any] = Depends(require_admin)
):
    update_data = template_update.dict(exclude_unset=True)
    updated_template = fruit_template_repo.update_template(template_id, **update_data)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Fruit template not found")
    return updated_template

@router.delete("/fruit-templates/{template_id}")
def delete_fruit_template(
    template_id: int,
    current_user: Dict[str, Any] = Depends(require_admin)
):
    if not fruit_template_repo.delete(template_id):
        raise HTTPException(status_code=404, detail="Fruit template not found")
    return {"message": "Fruit template deleted successfully"}