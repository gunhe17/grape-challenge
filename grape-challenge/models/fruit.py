from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import relationship
from ..database.database import Base

class FruitTemplate(Base):
    __tablename__ = "fruit_template"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, default='normal')
    seed_image = Column(Text)
    germination_image = Column(Text)
    seedling_image = Column(Text)
    juvenile_image = Column(Text)
    vegetative_image = Column(Text)
    reproductive_image = Column(Text)
    fruiting_image = Column(Text)

class Fruit(Base):
    __tablename__ = "fruit"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    template_id = Column(Integer, ForeignKey('fruit_template.id'), nullable=False)
    status = Column(String, default='씨앗')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    template = relationship("FruitTemplate", backref="fruits")