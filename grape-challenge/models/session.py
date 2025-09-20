from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import relationship
from ..database.database import Base

class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    fruit_id = Column(Integer, ForeignKey('fruit.id'), nullable=True)
    mission_ids = Column(Text, default='[]')  # JSON Array string
    status = Column(String, default='active')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", backref="sessions")
    fruit = relationship("Fruit", backref="session", uselist=False)