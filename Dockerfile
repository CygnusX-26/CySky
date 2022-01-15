FROM python:3.7-slim-buster

WORKDIR /app

COPY . .

RUN apt update &&   apt-get install python3-dev build-essential -y
RUN pip3 install -r requirements.txt
CMD ["python3", "/app/bot/discordBot.py"] 
