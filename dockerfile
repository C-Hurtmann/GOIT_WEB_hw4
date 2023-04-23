FROM python:3.10-slim

COPY . .

RUN mkdir -p storage

RUN touch storage/data.json

VOLUME [ "storage/data.json" ]

CMD ["python3", 'main.py']