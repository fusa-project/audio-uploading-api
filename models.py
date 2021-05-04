from database import Base
from sqlalchemy import Column, String, Boolean, Integer, Float, JSON, TIMESTAMP

class Audio(Base):
    __tablename__ = 'audio'
    id = Column(Integer, primary_key = True, autoincrement = True)
    filename = Column(String)
    file_path = Column(String)
    duration = Column(Float)
    size = Column(Float)
    data = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    recorded_at = Column(Integer)