import keyboards, funkfunctions, user, texts
import random
from aiogram.types import Message
from aiogram.filters import Text, Command


#Обработчик кнопки старт
@user.user.dp.message(Command(commands=['start']))
async def send_start_message(message : Message):
    await message.answer(texts.text.start_message,
                         reply_markup=keyboards.keyboard.keyboard_start)
    funkfunctions.funk.start_button(message)

#Обработчик кнопки инфо
@user.user.dp.message(Text(text=['info']))
async def send_info_message(message: Message):
    await message.answer(texts.text.info_bot_message,
                         reply_markup=keyboards.keyboard.keyboard_start)

#Обработчик кнопки задать время
@user.user.dp.message(Text(text = ['Установить таймер ⏲']))
async def send_timer_message(message: Message):
    print(user.user.user_info[message.from_user.id])
    if user.user.user_info[message.from_user.id]['timer'] == False :
        await message.answer(f'Выбери удобный переыв между сигаретами',
                         reply_markup=keyboards.keyboard.keyboard_smoke_time)
    else:

        await message.answer(f'Таймер уже запущен на {user.user.user_info[message.from_user.id]["time_for_minutes"]}\n\n'
                             f'Сбросить текуший и устаноить новый ?\n\n',
                             reply_markup=keyboards.keyboard.keyboard_yes_no)

@user.user.dp.message(Text(text=['1 час','2 часа','3 часа','4 часа']))
async def add_timer_message(message: Message):
    await message.answer(f'Я установил таймер на {message.text}',
                         reply_markup=keyboards.keyboard.keyboard_timer_on)
    funkfunctions.funk.add_new_timer_user_apdate(message)
    await funkfunctions.funk.restart_timer(message)


@user.user.dp.message(Text(text=['Да, сбросить таймер']))
async def reset_timer_message(message: Message):
    await message.answer(f'Выбери новое время',
                         reply_markup=keyboards.keyboard.keyboard_smoke_time)
    funkfunctions.funk.timer_reset(message)

@user.user.dp.message(Text(text=['Покурил 🚬']))
async def send_smoke_message(message : Message):

    if user.user.user_info[message.from_user.id]['timer'] == False:
        await message.answer(random.choice(user.user.user_info[message.from_user.id]['positive_answer']),
                         reply_markup=keyboards.keyboard.keyboard_timer_on)

        funkfunctions.funk.smoke_posutive(message)
        await funkfunctions.funk.restart_timer(message)
    else:
        await message.answer(random.choice(user.user.user_info[message.from_user.id]['negative_answer']),
                             reply_markup=keyboards.keyboard.keyboard_timer_on)
        funkfunctions.funk.smoke_negative(message)
        # запускаем таймер ожидания
        await funkfunctions.funk.restart_timer(message)

@user.user.dp.message(Text(text='Нет'))
async def back_to_back(message :Message):
    await message.answer('Окей, тогда ждем', reply_markup=keyboards.keyboard.keyboard_timer_on)

@user.user.dp.message(Text(text='Stat'))
async def statistic_info(message :Message):
    await message.answer(funkfunctions.funk.statistic_answer(message))

if __name__ =='__main__':
    user.user.dp.run_polling(user.user.bot)
