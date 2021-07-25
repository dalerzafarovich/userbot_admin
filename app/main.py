from aiogram import executor
from tgbot.config import dp
from tgbot.handlers.messages import register_messages
from userbot.config import userbot

register_messages(dp)

if __name__ == '__main__':
    try:
        executor.start_polling(dp)
    finally:
        userbot.stop()
