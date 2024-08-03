import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
from telebot import TeleBot
from telebot import types
from dotenv import load_dotenv
from itertools import batched
import os

URL = "https://w7.jujustu-kaisen.com/"
TIME_BETWEEN_CHECKS = timedelta(minutes=30)
SECONDARY_TIME = timedelta(minutes=5)

load_dotenv()
TOKEN = os.getenv("token")
CHAT_ID = os.getenv("chat-id")

bot = TeleBot(TOKEN)

def get_latest():
    site = requests.get(URL)
    print(f"{datetime.now().strftime("%H:%M").rjust(5)}: Request sent")
    return BeautifulSoup(site.text, "html.parser").find("li", {"id": "ceo_latest_comics_widget-3"}).find("ul").find("li").find("a")["href"]

def send(url):
    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")
    content = soup.find("div", {"class": "entry-content"})
    parags = content.find_all("p")
    pages = [parag.find("img")["data-src"] for parag in parags]
    files = [types.InputMediaPhoto(page, has_spoiler=True) for page in pages]
    bot.send_message(CHAT_ID, f"[New Chapter!]({url})", parse_mode='MARKDOWN')
    for group in batched(files, 10):
        bot.send_media_group(CHAT_ID, group)

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
        send(latest)
        latest = new