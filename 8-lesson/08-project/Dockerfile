FROM python:3.12-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
WORKDIR /app

RUN pip install -U pip

COPY reqs.txt .

RUN pip install -r reqs.txt

COPY . .

CMD "uvicorn -w 1 --host 0.0.0.0 --port 8000 app.server:get_app"


