# audio-uploading-api

Audio Uploading API for FuSA Project.

## Getting Started

### Installation and running
    ```
    docker-compose up --build
    ```

### Audio API
To enter the API, go to http://localhost:8000

This API will receive a POST method with audio metadata with this following structure:
```
{
    "id": int,
    "filename": str,
    "file_path": str,
    "duration": float,
    "size": float,
    "data": str,
    "latitude": float,
    "longitude": float,
    "recorded_at": int
}

```
### Database
You can enter to PGAdmin4 on http://localhost:5050/
The credentials are as follows:
```
user    : pgadmin4@pgadmin.org
password: admin
```

Inside PGAdmin4, you must create a server with this data:
```
- name    : fusa
- hostname: database
- username: admin
- password: 1234
```

### SSH
You can enter to the virtual docker filesystem:
```
docker ps
CONTAINER_ID   audio-uploading-api_api
```

Replace the CONTAINER_ID from audio-uploading-api_api IMAGE in the following command:
```
docker exec -it CONTAINER_ID bash
```

### RabbitMQ
In background, will be running RabbitMQ, so you can send data.

  * If you want to check if a data was sent, you can run ```python app/receive_audio.py```.
This will show the receiving information in the terminal.

## Other files
  * *audio.py*                 : it contains audio conversion functions.
  * *audio_queueing.py*        : it contains send_audio function for send the audio to RabbitMQ queue.
  * *receive_audio.py*         : RabbitMQ script that receive the audio input queue.
  * *test_audio_conversion.py* : a simple script for testing the audio conversion functions from audio.py.


## Authors

* Victor Vargas Sandoval victorvargassandoval93@gmail.com

## References

* RabbitMQ       - https://www.rabbitmq.com/#getstarted
* FastAPI        - https://fastapi.tiangolo.com/tutorial/
* Docker-compose - https://docs.docker.com/compose/