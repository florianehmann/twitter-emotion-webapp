FROM python:3.11-slim

RUN useradd twitter-emotion
WORKDIR /home/twitter-emotion

COPY requirements.txt requirements.txt
COPY app app
COPY app_entry.py gunicorn.conf.py boot.sh config.py ./
RUN chmod +x boot.sh

RUN chown -R twitter-emotion:twitter-emotion .

USER twitter-emotion

RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

ENV FLASK_APP app_entry.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
