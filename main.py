import asyncio
import datetime
import time
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.filters import Text, Command

TOKEN: str = '6059035440:AAGBNi_7ly8_jN5lNT_uitfv2tz6fbMBNxo'

bot: Bot = Bot(token = TOKEN)
dp: Dispatcher = Dispatcher()

user_info:dict = {'user_id' : None,
                  'timer': False,
                  'cigarettes': 0,
                  'time_for_minutes': 0,
                  'start_time' : None,
                  'finish_time' : None,
                  'new_timer_on' : False}
#Кнопки
button_time_edit: KeyboardButton = KeyboardButton(text='Установить таймер ⏲')
button_smoke: KeyboardButton = KeyboardButton(text='Покурил 🚬')
button_info: KeyboardButton = KeyboardButton(text= 'info')
button_time_1: KeyboardButton = KeyboardButton(text='1 час')
button_time_2: KeyboardButton = KeyboardButton(text='2 часа')
button_time_3: KeyboardButton = KeyboardButton(text='3 часа')
button_time_4: KeyboardButton = KeyboardButton(text='4 часа')
button_yes: KeyboardButton = KeyboardButton(text = 'Да, сбросить таймер')
button_no: KeyboardButton = KeyboardButton(text='Нет')


#создаем обьект клавиатуры (по кнопке старт)
keyboard_start: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_info, button_time_edit]],
                                                           resize_keyboard=True)
#создаем обьект клавиатуры (Установи таймер)
keyboard_smoke_time: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_time_1, button_time_2,
                                                                             button_time_3, button_time_4]],
                                                                resize_keyboard=True)
#создаем обьект клавиатуры (После установки времени)
keyboard_timer_on: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_time_edit, button_smoke]],
                                                       resize_keyboard=True)
#создаем обьект клавиатуры (Для изменения времени таймера)
keyboard_yes_no: ReplyKeyboardMarkup =ReplyKeyboardMarkup(keyboard=[[button_yes, button_no]],
                                                          resize_keyboard=True)
#фунция перевода введенного времени в значения
def translate_of_time(time:str) -> int:
    if time == '1 час':
        return 10
    elif time == '2 часа':
        return 10
    elif time == '3 часа':
        return 10
    elif time == '4 часа':
        return 10

#Фунция повторения таймера -для случаев когда клиент покурил после таймера или во время таймера
async def restart_timer(message: Message):
    user_info[message.from_user.id]['timer'] = True
    new_time = user_info[message.from_user.id]['time_for_minutes']
    await asyncio.sleep(new_time)
    await bot.send_message(message.from_user.id,
                        f'Таймер на {user_info[message.from_user.id]["time_for_minutes"]} секунд закончился')
    user_info[message.from_user.id]['timer'] = False

#Обработчик кнопки старт
@dp.message(Command(commands=['start']))
async def send_start_message(message : Message):
    await message.answer(f'Привет 🙌, я могу помочь в борьбе с курением! \n'
                         f'Укажи вермя перерыва между сигаретами, я буду напоминать тебе когда таймер подойтет к концу\n',
                         reply_markup=keyboard_start)
    if message.from_user.id not in user_info:
        user_info[message.from_user.id] = {
                  'timer': False,
                  'cigarettes': 0,
                  'time_for_minutes': 0,
                  'start_time' : None,
                  'finish_time' : None}

#Обработчик кнопки инфо
@dp.message(Text(text=['info']))
async def send_info_message(message: Message):
    await message.answer(f'Смотри, все просто🥱\n\n'
                         f'Выбераешь время таймера и стараешься не курить⏲\n\n'
                         f'Если покурил - не страшно, просто сообщи мне и я сброшу таймер и мы попробуем заново🤓\n\n'
                         f'Если таймер кончится я сообщу о том что можно устроить перекур🚬\n\n'
                         f'Если выбрал слишком большой перерыв, всегда можешь поменять его⚙\n\n'
                         f'Давай попробуем💪',
                         reply_markup=keyboard_start)

#Обработчик кнопки задать время
@dp.message(Text(text = ['Установить таймер ⏲']))
async def send_timer_message(message: Message):
    print(user_info[message.from_user.id])
    if user_info[message.from_user.id]['timer'] == False :
        await message.answer(f'Выбери удобный переыв между сигаретами',
                         reply_markup=keyboard_smoke_time)
    else:

        await message.answer(f'Таймер уже запущен на {user_info[message.from_user.id]["time_for_minutes"]}\n\n'
                             f'Сбросить текуший и устаноить новый ?\n\n',
                             reply_markup=keyboard_yes_no)

@dp.message(Text(text=['1 час','2 часа','3 часа','4 часа']))
async def add_timer_message(message: Message):

    await message.answer(f'Я установил таймер',
                         reply_markup=keyboard_timer_on)
    user_info[message.from_user.id]['timer'] = True  #устанавливаем флаг что таймер включен
    user_info[message.from_user.id]['time_for_minutes'] = translate_of_time(message.text)
    print(user_info[message.from_user.id]['time_for_minutes'])
    print(user_info[message.from_user.id])
    #запускаем таймер ожидания
    while user_info[message.from_user.id]['timer'] == True :
        await asyncio.sleep(user_info[message.from_user.id]['time_for_minutes'])
        await bot.send_message(message.from_user.id, f'Таймер на {user_info[message.from_user.id]["time_for_minutes"]} секунд закончился')
        user_info[message.from_user.id]['timer'] = False
        print(user_info[message.from_user.id])

@dp.message(Text(text=['Да, сбросить таймер']))
async def reset_timer_message(message: Message):
    await message.answer(f'Выбери новое время',
                         reply_markup=keyboard_smoke_time)
    user_info[message.from_user.id]['timer'] = False

@dp.message(Text(text=['Покурил 🚬']))
async def send_smoke_message(message : Message):

    if user_info[message.from_user.id]['timer'] == False:
        await message.answer(f'Круто что получилось продержаться\n\n'
                         f'Я завел его опять на такое же время',
                         reply_markup=keyboard_timer_on)
        user_info[message.from_user.id]['cigarettes'] += 1
        await restart_timer(message)
        print(user_info[message.from_user.id])
    else:
        await message.answer(f'Не перживай\n\n'
                             f'Я завел его опять на такое же время',
                             reply_markup=keyboard_timer_on)
        user_info[message.from_user.id]['cigarettes'] += 1
        user_info[message.from_user.id]['timer'] = False
        print(user_info[message.from_user.id])
        await restart_timer(message)

if __name__ =='__main__':
    dp.run_polling(bot)