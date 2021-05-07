import pika
import json

class AudioQueueing:    
    @staticmethod
    def send_audio(host, data):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        channel = connection.channel()
        channel.queue_declare(queue='audio_input')

        channel.basic_publish(exchange='',
                            routing_key='audio_input',
                            body=json.dumps(data))
        connection.close()