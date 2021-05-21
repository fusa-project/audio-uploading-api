import pika, sys, os
from .database import SessionLocal, engine, get_db
from .schemas import Audio
from . import models

models.Base.metadata.create_all(bind=engine)
db = get_db()

QUEUE_NAME = "audio_input"

def main():
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

if __name__ == '__main__':
    main()