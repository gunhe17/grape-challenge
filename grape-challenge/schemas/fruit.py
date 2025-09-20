from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FruitBase(BaseModel):
    template_id: int
    status: str = '씨앗'

class FruitCreate(FruitBase):
    pass

class FruitUpdate(BaseModel):
    template_id: Optional[int] = None
    status: Optional[str] = None

class FruitRead(FruitBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class FruitStatusUpdate(BaseModel):
    status: str

class FruitTemplateBase(BaseModel):
    name: str
    type: str = 'normal'
    seed_image: Optional[str] = None
    germination_image: Optional[str] = None
    seedling_image: Optional[str] = None
    juvenile_image: Optional[str] = None
    vegetative_image: Optional[str] = None
    reproductive_image: Optional[str] = None
    fruiting_image: Optional[str] = None

class FruitTemplateCreate(FruitTemplateBase):
    pass

class FruitTemplateUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    seed_image: Optional[str] = None
    germination_image: Optional[str] = None
    seedling_image: Optional[str] = None
    juvenile_image: Optional[str] = None
    vegetative_image: Optional[str] = None
    reproductive_image: Optional[str] = None
    fruiting_image: Optional[str] = None

class FruitTemplateRead(FruitTemplateBase):
    id: int
    
    class Config:
        from_attributes = True

class FruitProgress(BaseModel):
    fruit_id: int
    template_id: int
    template_name: str
    current_image: Optional[str]
    growth_stage: str
    mission_count: int
    progress_percentage: float