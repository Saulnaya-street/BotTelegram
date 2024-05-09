import telebot
from config import keys, TOKEN
from extensions import MoneyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = ('Чтобы начать работу введите команду боту в следующем формате: \n'
            '<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену> <количество первой валюты>\n'
            'Увидеть список всех доступных валют: /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text += f'\n{key}'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        args = message.text.split()

        if len(args) != 3:
            raise APIException("Неправильный формат запроса. Используйте формат: <валюта из> <валюта в> <количество>.")

        quote, base, amount = args
        total_base = MoneyConverter.get_price(quote, base, amount)
        text = f'Цена {amount} {quote} в {base} составляет {total_base} {base}'
    except APIException as e:
        bot.reply_to(message, str(e))
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка на сервере:\n{e}")
    else:
        bot.send_message(message.chat.id, text)



bot.polling()




