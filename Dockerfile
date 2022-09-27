FROM python:3.9-slim-bullseye

RUN python3 -m venv /opt/venv

COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip3 install -r requirements.txt

COPY . /app
CMD . /opt/venv/bin/activate && exec python app/main.py