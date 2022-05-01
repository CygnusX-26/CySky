FROM python:3.7-slim-buster

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
RUN apt-get install git
RUN pip3 install -U git+https://github.com/Rapptz/discord.py
CMD ["python3", "/app/bot/discordBot.py"] 
