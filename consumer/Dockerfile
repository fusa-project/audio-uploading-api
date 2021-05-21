FROM python:3.7-alpine

RUN mkdir /app
COPY receiver.py /app/receiver.py
COPY retry.py /app/retry.py
COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip --no-cache-dir install -r requirements.txt
CMD ["python", "main.py"]