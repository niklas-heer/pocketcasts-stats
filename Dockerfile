# See https://hub.docker.com/r/library/python/
FROM python:3.7-alpine

LABEL Name=pocketcasts-stats

WORKDIR /app
COPY . /app

# Using pip:
RUN python3 -m pip install -r requirements.txt
CMD ["python3", "./app.py"]
