FROM python:3.10

WORKDIR /GOIT_WEB_hw4

COPY . .

RUN pip install requests

CMD ["python3", 'main.py']