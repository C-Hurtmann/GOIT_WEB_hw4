FROM python:3.10-slim-buster

WORKDIR .

COPY . .

VOLUME ./storage

EXPOSE 3000

CMD ["python3", "main.p