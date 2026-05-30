from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_path = Column(String, nullable=False)
    description = Column(String, nullable=True)
    keywords = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
