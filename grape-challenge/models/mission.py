from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import relationship
from ..database.database import Base

class MissionTemplate(Base):
    __tablename__ = "mission_template"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, default='normal')
    content = Column(Text, nullable=False)

class Mission(Base):
    __tablename__ = "mission"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    template_id = Column(Integer, ForeignKey('mission_template.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    status = Column(String, default='pending')
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    template = relationship("MissionTemplate", backref="missions")
    user = relationship("User", backref="missions")