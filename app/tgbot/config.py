from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

from app.config import bot_token, redis_config

bot = Bot(bot_token)
storage = RedisStorage(**redis_config)

dp = Dispatcher(bot, storage=storage)
