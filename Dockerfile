FROM python:3.10

COPY . .

VOLUME [ "/storage" ]

CMD python3 main.py