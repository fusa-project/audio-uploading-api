import pika
import json

class AudioQueueing:    
    @staticmethod
    def send_audio(host, queue, data):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        channel = connection.channel()
        channel.queue_declare(queue=queue)

        channel.basic_publish(exchange='',
                            routing_key=queue,
                            body=json.dumps(data))
        connection.close()