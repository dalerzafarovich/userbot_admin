from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import emoji

from app.config import bot_name, channel_id, userbot_id
from app.userbot.config import userbot
from app.tgbot.config import bot

userbot.start()


class SendMessageStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_message = State()
    confirmation = State()


async def start(m: types.Message):
    await m.answer('Под каким именем вы хотите отправить пост на канал?')
    await SendMessageStates.waiting_for_username.set()


async def username_setting(m: types.Message, state: FSMContext):
    username = m.text
    if len(username) > 20:
        await m.answer('Слишком длинное имя')
    await state.update_data(username=username)
    await m.answer('Отправьте сообщение')
    await SendMessageStates.next()


async def message_text(m: types.Message, state: FSMContext):
    await state.update_data(message_id=m.message_id)
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton('Отправить', callback_data='send'),
        types.InlineKeyboardButton('Отмена', callback_data='cancel')
    ]
    keyboard.add(*buttons)
    username = (await state.get_data()).get('username')
    await m.answer(f'<b>Username: </b>{username}', parse_mode='HTML')
    await m.send_copy(m.from_user.id)
    await m.answer('Подтвердите отправку сообщения', reply_markup=keyboard)
    await SendMessageStates.next()


async def confirmation(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username, m_id = data['username'], data['message_id']
    await bot.copy_message(userbot_id, callback.from_user.id, m_id)
    await userbot.update_profile(first_name=username)
    message = (await userbot.get_history(bot_name, 1))[0]
    await userbot.copy_message(channel_id, bot_name, message.message_id)
    await userbot.update_profile(first_name='Userbot')
    await callback.answer()
    await callback.message.edit_text('Сообщение отправлено')
    await state.finish()


async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Операция отменена')
    await callback.answer()
    await state.finish()


def register_messages(dp: Dispatcher):
    dp.register_message_handler(start, commands='send_message', state='*')
    dp.register_message_handler(username_setting, state=SendMessageStates.waiting_for_username)
    dp.register_message_handler(message_text, state=SendMessageStates.waiting_for_message,
                                content_types=types.ContentTypes.all())
    dp.register_callback_query_handler(confirmation, text='send', state=SendMessageStates.confirmation)
    dp.register_callback_query_handler(cancel, text='cancel', state=SendMessageStates.confirmation)
