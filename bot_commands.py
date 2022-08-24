from config import *
from CurrencyValues import CurrencyValues

cv = CurrencyValues(url)


@bot.message_handler(commands=['start', 'help'])
def func(message):
    bot.send_message(message.chat.id, cv.info())


@bot.message_handler(commands=['values'])
def func(message):
    count = 0
    result_str = 'Код валюты: описание\n'
    for key, value in cv.list_of_values.items():
        result_str += f'{key}: Валюта {value[0]} из страны {value[1]}\n'
        if count == 50:
            bot.send_message(message.chat.id, result_str)
            result_str = ''
            count = 0
        count += 1
    bot.send_message(message.chat.id, f'{result_str}Итого: {cv.count_of_values}')


@bot.message_handler(content_types='text')
def func(message):
    try:
        base, quote, _amount = message.text.split()
        amount = int(_amount)
    except Exception as e:
        bot.send_message(message.chat.id, f'Упс, ошибка. Неверный формат ввода. \n'
                                          f'Подробное описание ошибки:{e}\n'
                                          f'Верная последовательность: "Валюта1 Валюта2 Количество"\n'
                                          f'Список валют вы можете получить по команде /values')
        return None
    if cv.exchange_currency(base, quote, amount):
        bot.send_message(message.chat.id, cv.format_str)
    else:
        bot.send_message(message.chat.id, f'Упс, ошибка. Неверный код валюты')
