import time

from aiogram import Bot, Dispatcher

TOKEN: str = '6059035440:AAGBNi_7ly8_jN5lNT_uitfv2tz6fbMBNxo'
bot: Bot = Bot(token = TOKEN)
dp: Dispatcher = Dispatcher()


user_info: dict = {'user_id': None,
                  'timer': False,
                  'cigarettes_on_timer': 0,
                 'cigarettes_off_timer': 0,
                  'time_for_seconds': 0,
                  'start_time': None,
                  'finish_time': None,
                  'new_timer_on': False,
                  'count_clock': 0,
                    'positive_answer': [],
                   'negative_answer': []
                   }
