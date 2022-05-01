FROM python:3.8-slim-buster

WORKDIR /app

COPY . .
RUN apt-get update && apt-get install -y git
RUN pip3 install -U git+https://github.com/Rapptz/discord.py
RUN pip3 install -r requirements.txt
CMD ["python3", "/app/bot/discordBot.py"] 
