import user, asyncio, time
from aiogram.types import Message



# фунция перевода введенного времени в секунды
def translate_of_time(time: str) -> int:
    if time == '1 час':
        return 30
        #return 60 ** 2
    elif time == '2 часа':
        return (60 ** 2) * 2
    elif time == '3 часа':
        return (60 ** 2) * 3
    elif time == '4 часа':
        return (60 ** 2) * 4

# фунция перевода введенного времени в часы
def translate_for_hour(time:int) -> str:
    if time == 30:
        return '1 час'
    elif time == (60 ** 2) * 2:
        return '2 часа'
    elif time == (60 ** 2) * 3:
        return '3 часа'
    elif time == (60 ** 2) * 4:
        return '4 часа'


# Фунция повторения таймера -для случаев когда клиент покурил после таймера или во время таймера
async def restart_timer(message: Message):
    user.user.user_info[message.from_user.id]['timer'] = True
    new_time = user.user.user_info[message.from_user.id]['time_for_seconds']
    user.user.user_info[message.from_user.id]['finish_time'] = time.time() + user.user.user_info[message.from_user.id]['time_for_seconds']
    await asyncio.sleep(new_time)
    # проверка на количество вызовов
    if user.user.user_info[message.from_user.id]['count_clock'] > 1:
        print(user.user.user_info[message.from_user.id]['count_clock'])
        user.user.user_info[message.from_user.id]['count_clock'] -= 1
        print(user.user.user_info[message.from_user.id]['count_clock'])

    elif user.user.user_info[message.from_user.id]['new_timer_on'] == True:
        user.user.user_info[message.from_user.id]['new_timer_on'] = False
        user.user.user_info[message.from_user.id]['count_clock'] = 0
        print('tyt')
    else:
        await user.user.bot.send_message(message.from_user.id,
                                         f'Таймер на {user.user.user_info[message.from_user.id]["time_for_seconds"]} секунд закончился')
        user.user.user_info[message.from_user.id]['count_clock'] = 0
        user.user.user_info[message.from_user.id]['timer'] = False

# функция кнопки старт
def start_button(message):
    if message.from_user.id not in user.user.user_info:
        user.user.user_info[message.from_user.id] = {
            'timer': False,
            'cigarettes_on_timer': 0,
            'cigarettes_off_timer': 0,
            'time_for_seconds': 0,
            'start_time': None,
            'finish_time': None,
            'new_timer_on': False,
            'count_clock': 0
        }

def add_new_timer_user_apdate(message):
    user.user.user_info[message.from_user.id]['timer'] = True  # устанавливаем флаг что таймер включен
    user.user.user_info[message.from_user.id]['new_timer_on'] = False
    user.user.user_info[message.from_user.id]['time_for_seconds'] = translate_of_time(message.text)
    user.user.user_info[message.from_user.id]['finish_time'] = time.time() + translate_of_time(message.text)
    print(user.user.user_info[message.from_user.id]['time_for_seconds'])
    print(user.user.user_info[message.from_user.id])
    print(user.user.user_info[message.from_user.id]['start_time'])
    print(user.user.user_info[message.from_user.id]['finish_time'])
    # добавляем значение зпущенного таймера

    user.user.user_info[message.from_user.id]['count_clock'] += 1

def timer_reset(message):
    user.user.user_info[message.from_user.id]['timer'] = False
    user.user.user_info[message.from_user.id]['new_timer_on'] = True


def statistic_answer(message):
    return f'Колличество перекуров по таймеру = {user.user.user_info[message.from_user.id]["cigarettes_on_timer"]}\n\n' \
           f'Колличество перекуров вне таймера = {user.user.user_info[message.from_user.id]["cigarettes_off_timer"]}\n\n' \
           f'Всего перекуров = {user.user.user_info[message.from_user.id]["cigarettes_on_timer"] + user.user.user_info[message.from_user.id]["cigarettes_off_timer"]}\n\n'\
           f'Время до конца таймера {time_left(message)}'

def smoke_posutive(message):
    user.user.user_info[message.from_user.id]['cigarettes_on_timer'] += 1
    # добавляем значение зпущенного таймера
    user.user.user_info[message.from_user.id]['count_clock'] += 1

def smoke_negative(message):
    user.user.user_info[message.from_user.id]['cigarettes_off_timer'] += 1
    user.user.user_info[message.from_user.id]['timer'] = False
    user.user.user_info[message.from_user.id]['count_clock'] += 1

#оставшееся время
def time_left(message):
    left_time = user.user.user_info[message.from_user.id]['finish_time'] - time.time()
    result = time.gmtime(left_time)
    return f'{result.tm_hour}:{result.tm_min}:{result.tm_sec}'
