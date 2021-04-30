from fastapi import FastAPI
from pydantic import BaseModel
import datetime
from audio_queueing import AudioQueueing

queue = AudioQueueing()

app = FastAPI()

db = []

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

@app.get("/")
def index():
    return {"greetings": "Welcome to FUSA"}

@app.get("/health")
def health():
    return {"status": "200"}

@app.get("/audio")
def get_audios():
    return db

@app.get("/audio/{audio_id}")
def get_audio(audio_id: int):
    audio = audio_id - 1
    return db[audio]

@app.post("/add_audio")
async def add_audio(audio: Audio):
    data = audio.dict()
    db.append(data)
    host = "localhost"
    queue.send_audio(host, data)
    return db[-1]

@app.delete("/audio/{audio_id}")
def delete_audio(audio_id: int):
    db.pop(audio_id - 1)
    return {"task": "deletion successful"}