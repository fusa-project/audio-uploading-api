from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import datetime
from .audio_queueing import AudioQueueing
from .database import SessionLocal, engine, get_db
from .schemas import Audio
from . import models

models.Base.metadata.create_all(bind=engine)
queue = AudioQueueing()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def index():
    return {"greetings": "Welcome to FUSA"}

@app.get("/health")
def health():
    return {"status": "200"}

@app.get("/audio/}")
def get_audios(db=Depends(get_db)):
    return db.query(models.Audio).all()

@app.get("/audio/{audio_id}")
def get_audio(audio_id: int, db=Depends(get_db)):
    audio = db.query(models.Audio).filter(
        models.Audio.id == audio_id).first()
    if audio:
        return audio
    else:
        raise HTTPException(
            status_code=404,
            detail=f'No audio found for id {audio_id}')

@app.post("/add_audio/")
async def add_audio(audio: Audio, db=Depends(get_db)):
    audio_dict = audio.dict()
    try:
        host = "rabbitmq"
        queue.send_audio(host, audio_dict)
        new_audio = models.Audio(**audio_dict)
        db.add(new_audio)
        db.commit()
        db.refresh(new_audio)
        return new_audio
    except Exception as e:
        print(e)

        raise HTTPException(
            status_code=400,
            detail='This audio already exists')

@app.delete("/delete_audio/{audio_id}}")
def delete_audio(audio_id: int, db=Depends(get_db)):
    audio = db.query(models.Audio).filter(
        models.Audio.id == audio_id)
    if audio.first():
        audio.delete(synchronize_session=False)
        db.commit()
        return f'Audio {audio_id} deleted succesfully'
    else:
        raise HTTPException(
            status_code=404,
            detail=f'No audio found for id {audio_id}')