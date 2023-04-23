FROM python:3.10

COPY . .

VOLUME [ "/storage" ]

EXPOSE 3000

CMD python3 main.py