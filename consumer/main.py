import pika, sys, os
from database import SessionLocal, engine, get_db
from schemas import Audio
from database import Base
from sqlalchemy import Column, String, Boolean, Integer, Float, JSON, TIMESTAMP
import time

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

Base.metadata.create_all(bind=engine)
db = get_db()

QUEUE_NAME = "audio_input"

def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)

        def parse_audio(ch, method, properties, body):
            audio = Audio().parse_obj(json.loads(body))
            new_audio = models.Audio(**audio.dict())
            db.add(new_audio)
            db.commit()
            db.refresh(new_audio)
            print(f"Received Audio: {audio.filename}")

        channel.basic_consume(queue=QUEUE_NAME,
                            on_message_callback=parse_audio,
                            auto_ack=True)

        print(f"Starting to receive messages from queue: {QUEUE_NAME}")
        channel.start_consuming()
    except Exception:
        sleep_time = 5
        print(f"Error listening at RabbitMQ, retrying in {sleep_time} seconds...")
        time.sleep(sleep_time)

if __name__ == '__main__':
    while True:
        main()