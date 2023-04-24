FROM python:3.10

ENV APP_HOME /app

WORKDIR ${APP_HOME}

COPY . .

EXPOSE 3000

VOLUME /app/storage

ENTRYPOINT [ "python3", "main.py" ]