#!/usr/bin/env python
import pika, sys, os
import json
from audio import AudioProcessing as ap

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='audio_input')

    def callback(ch, method, properties, body):
        dic = json.loads(body)
        print(f" [x] Received {dic['filename']}")

    channel.basic_consume(queue='audio_input', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)