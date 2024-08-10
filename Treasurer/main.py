from telebot import TeleBot
import requests
from dotenv import load_dotenv
import gspread
from datetime import datetime, timedelta
import os
import re

load_dotenv()
TOKEN = os.getenv("token")
KEY = os.getenv("spreadsheet")
DAY = timedelta(1)
WEEK = timedelta(7)
CURRENCIES_URL = "https://fxds-public-exchange-rates-api.oanda.com/cc-api/currencies"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Site": "same-site"
}

def get_params(base: str, quote: str):
    start = (datetime.today() - WEEK).strftime("%Y-%m-%d")
    end = (datetime.today() - DAY).strftime("%Y-%m-%d")
    return {"base": base, "quote": quote, "data_type": "chart", "start_date": start, "end_date": end}

def number(num: str) -> float:
    return float(num.replace(",", ".", 1).replace("\xa0", ""))

file = gspread.oauth().open_by_key(KEY)

def pound_handler(cost, p2d, d2s):return [cost, cost*p2d, cost*p2d*d2s]
def dollar_handler(cost, p2d, d2s):return [cost/p2d, cost, cost*d2s]
def som_handler(cost, p2d, d2s):return [cost/d2s/p2d, cost/d2s, cost]

currencies = {"p": pound_handler, "d": dollar_handler, "s": som_handler,
              "ф": pound_handler, "д": dollar_handler, "с": som_handler}
months = [None, "январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]


bot = TeleBot(TOKEN)

def new_currencies() -> tuple[float, float]:
    return (
        requests.get(CURRENCIES_URL, params=get_params("GBP", "USD"), headers=HEADERS).json()["response"][-1]["average_bid"],
        requests.get(CURRENCIES_URL, params=get_params("USD", "KGS"), headers=HEADERS).json()["response"][-1]["average_bid"])

def new_month(sh1: gspread.worksheet.Worksheet, month: str):
    data = sh1.get("A1:F6")
    sh = file.add_worksheet(month, 26, 500, 0)
    sh.update(data, "A1:F6")
    new_pound, new_dollar = new_currencies()
    sh.update(new_dollar, sh.find("dollar").address)
    sh.update(new_pound, sh.find("pound").address)
    return sh

def parse_entry(text):
    data: list[str] = text.split()
    if data[-1] not in currencies:
        data.append("p")
    print(data)
    data = (" ".join(data[:-2]), *data[-2:])
    print(data)
    if not re.match(r"^[\d,\.]+$", data[1]):
        return None
    return data

@bot.message_handler(commands=["quit"])
def stop(message):
    bot.reply_to(message, "Stopping")
    bot.stop_polling()
    quit()

@bot.message_handler(commands=["url"])
def get_url(message):
    bot.reply_to(message, f"https://docs.google.com/spreadsheets/d/{file.id}")

def delete_last(sh: gspread.worksheet.Worksheet):
    anchor = sh.find("anchor")
    x, y = anchor.col, anchor.row
    x+=2
    while sh.cell(y, x).value: y+=1
    return sh.cell(y-1, x)

@bot.message_handler(commands=["delete"])
def delete(message):
    reply = message.reply_to_message
    sh = file.sheet1
    if reply is None:
        entry = delete_last(sh)
    else:
        entry = sh.find(parse_entry(reply.text)[0])
    sh.delete_rows(entry.row)
    bot.reply_to(message, "Deleted")

@bot.message_handler()
def add(message):
    data = parse_entry(message.text)
    if data is None:
        bot.reply_to(message, "Parsing error: Cost not recognised")
        return
    date = datetime.fromtimestamp(message.date)
    sh = file.sheet1
    if months[date.month] != sh.title:
        sh = new_month(sh, months[date.month])
    dollar = sh.find("dollar")
    pound = sh.find("pound")
    dollar2som = number(sh.cell(dollar.row, dollar.col-1).value)
    pound2dollar = number(sh.cell(pound.row, pound.col-1).value)
    costs = currencies[data[2]](number(data[1]), pound2dollar, dollar2som)
    sync(sh, date, data[0], costs)
    bot.reply_to(message, "Updated")

def sync(sh: gspread.worksheet.Worksheet, date: datetime, desc: str, costs: list[int]):
    anchor = sh.find("anchor")
    x, y = anchor.col, anchor.row
    x+=1
    while sh.cell(y, x).value: y+=1
    sh.copy_range(f"B{y}:F{y}", f"B{y+2}:F{y+2}")
    sh.copy_range(f"B{y+1}:F{y+1}", f"B{y+3}:F{y+3}")
    sh.delete_rows(y+1)
    sh.update([[f"{date.month}/{date.day}", desc, *costs]], f"B{y}:F{y}", value_input_option='USER_ENTERED')


bot.polling()