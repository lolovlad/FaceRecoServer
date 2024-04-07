FROM python:3.10
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN chmod a+x docker/*.sh

