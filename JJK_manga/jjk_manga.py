import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
from telebot import TeleBot
from dotenv import load_dotenv
import os

URL = "https://ww2.jujustukaisen.com/"
TIME_BETWEEN_CHECKS = timedelta(minutes=30)
SECONDARY_TIME = timedelta(minutes=5)

load_dotenv()
TOKEN = os.getenv("token")
CHAT_ID = int(os.getenv("chat-id"))

bot = TeleBot(TOKEN)

def get_latest():
    site = requests.get(URL)
    print(f"{datetime.now().strftime("%H:%M").rjust(5)}: Request sent")
    return BeautifulSoup(site.text, "html.parser").find("li", {"id": "ceo_latest_comics_widget-3"}).find("ul").find("li").find("a")["href"]

def send(text):
    bot.send_message(CHAT_ID, text)

def wait4check():
    while last_check + TIME_BETWEEN_CHECKS > datetime.now():
        sleep(SECONDARY_TIME.total_seconds())

latest = new = get_latest()
last_check = datetime.now()
while True:
    wait4check()
    try:
        new = get_latest()
    except ConnectionError:
        print("Request failed")
        continue
    last_check = datetime.now()
    if latest != new:
        print(f"New chapter detected! ({new})")
        latest = new
        send(latest)
