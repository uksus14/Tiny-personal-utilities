import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
from telebot import TeleBot
from dotenv import load_dotenv
import os

URL = "https://ww2.jujustukaisen.com/"
TIME_BETWEEN_CHECKS = timedelta(hours=1)

load_dotenv()
TOKEN = os.getenv("token")
CHAT_ID = int(os.getenv("chat-id"))

bot = TeleBot(TOKEN)
last_check = datetime.now()

def get_latest():
    return BeautifulSoup(requests.get(URL).text, "html.parser").find("li", {"id": "ceo_latest_comics_widget-3"}).find("ul").find("li").find("a")["href"]

def send(text):
    bot.send_message(CHAT_ID, text)

latest = get_latest()
while True:
    new = get_latest()
    if latest != new:
        latest = new
        send(latest)
    while last_check + TIME_BETWEEN_CHECKS > datetime.now():
        sleep(10*60)
