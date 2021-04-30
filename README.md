# audio-uploading-api

Audio Uploading API for FuSA Project.

## Getting Started

### Installation
    ```
    python -m pip install --user virtualenv
    virtualenv ENV_NAME

    source ENV_NAME/bin/activate

    pip install -r requirements.txt
    ```

### Run the example app
    ```
    uvicorn test:app --reload
    ```
Then, enter on http://127.0.0.1:8000


### Run the audio API and send data to RabbitMQ
First, you must run the Docker with the RabbitMQ local Server:
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Then, run the API with the following:
```
uvicorn audio_api:app --reload
```

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

If a request was ok, the api will send the data to the RabbitMQ queue

  * If you want to check if the data was sent, you can run ```python receive_audio.py```.
This will show the receiving information in the terminal.

## Other files
  * *audio.py*                 : it contains audio conversion functions.
  * *audio_queueing.py*        : it contains send_audio function for send the audio to RabbitMQ queue.
  * *receive_audio.py*         : RabbitMQ script that receive the audio input queue.
  * *test_audio_conversion.py* : a simple script for testing the audio conversion functions from audio.py.


## Authors

* Victor Vargas Sandoval victorvargassandoval93@gmail.com

## References

* RabbitMQ - https://www.rabbitmq.com/#getstarted
* FastAPI - https://fastapi.tiangolo.com/tutorial/