FROM python:3.7-slim-buster

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "/app/bot/discordBot.py"] 
