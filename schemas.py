from pydantic import BaseModel

class Audio(BaseModel):
    id: int
    filename: str
    file_path: str
    duration: float
    size: float
    data: str
    latitude: float
    longitude: float
    recorded_at: int

    class Config():
        orm_mode = True