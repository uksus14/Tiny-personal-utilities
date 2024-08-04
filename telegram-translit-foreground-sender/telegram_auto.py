from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
MY_PHONE = os.getenv('MY_PHONE')

default_user = MY_PHONE

async def login(client, phone_number):
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        code = input('Enter the code you received: ')
        await client.sign_in(phone_number, code)

async def full_send(user, text):
    async with TelegramClient('Adil', API_ID, API_HASH) as client:
        await login(client, MY_PHONE)
        await client.send_message(user, text)
        print("message sent")