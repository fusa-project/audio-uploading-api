import pika, sys, os
from schemas import PyAudio
from sqlalchemy import Column, String, Boolean, Integer, Float, JSON, TIMESTAMP
import time
import logging
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

Base = declarative_base()

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

SQLALCHEMY_DATABASE_URL = "postgresql://admin:1234@localhost:5432/fusa"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
db = SessionLocal()

QUEUE_NAME = "audio_input"

def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)

        def parse_audio(ch, method, properties, body):
            body_data = json.loads(body)
            audio = PyAudio.parse_obj(body_data)
            new_audio = Audio(**audio.dict())
            db.add(new_audio)
            db.commit()
            db.refresh(new_audio)
            logging.info("Received Audio")

        channel.basic_consume(queue=QUEUE_NAME,
                            on_message_callback=parse_audio,
                            auto_ack=True)

        logging.info(f"Starting to receive messages from queue: {QUEUE_NAME}")
        channel.start_consuming()
    
    except pika.exceptions.AMQPConnectionError:
        sleep_time = 5
        logging.info(f"Error listening at RabbitMQ, retrying in {sleep_time} seconds...")
        time.sleep(sleep_time)

    except Exception:
        logging.error("Error listening messages", exc_info=True)

if __name__ == '__main__':
    while True:
        main()