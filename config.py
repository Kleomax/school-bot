from dotenv import load_dotenv
import os

from aiogram import Bot


ProductionMode = False
ExamsInfo = False


load_dotenv()

if ProductionMode == True:
    BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")
    HOST = os.getenv("MAIN_HOST")
    USER = os.getenv("MAIN_USER")
    PASSWORD = os.getenv("MAIN_PASSWORD")
    DB_NAME = os.getenv("MAIN_DB_NAME")

    admins = os.getenv("MAIN_ADMINS", "").split(",")
    admins_list = [int(admin.strip()) for admin in admins if admin.strip()]

else:
    BOT_TOKEN = os.getenv("TEST_BOT_TOKEN")
    HOST = os.getenv("TEST_HOST")
    USER = os.getenv("TEST_USER")
    PASSWORD = os.getenv("TEST_PASSWORD")
    DB_NAME = os.getenv("TEST_DB_NAME")

    admins = os.getenv("TEST_ADMINS", "").split(",")
    admins_list = [int(admin.strip()) for admin in admins if admin.strip()]

KEYS = os.getenv("API_KEYS").split(",")
API_KEYS = [key.strip() for key in KEYS if key.strip()]

system_prompt = ''

bot = Bot(BOT_TOKEN)
