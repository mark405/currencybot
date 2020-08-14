import telebot
import schedule
import sqlite3
from time import sleep
from telebot import types
from telebot.util import async_dec
import config
from mainmain import convert_dollar, convert_euro, convert_pound, \
    convert_bitcoin, convert_rubl, convert_frank, convert_canadadollar, \
    convert_yen, convert_ausdollar, convert_ether, convert_israel, convert_litecoin, \
    convert_bitcoin_dollar, convert_ether_dollar, convert_litecoin_dollar
from mainrus import convert_rus_dollar, convert_rus_euro, convert_rus_pound, \
    convert_rus_bitcoin, convert_rus_grivna, convert_rus_frank, convert_rus_canadadollar, \
    convert_rus_yen, convert_rus_ausdollar, convert_rus_ether, convert_rus_israel, convert_rus_litecoin, \
    convert_litecoin_euro, convert_ether_euro, convert_bitcoin_euro

bot = telebot.TeleBot(config.TOKEN)

con = sqlite3.connect("id2.db", check_same_thread=False)

cursor = con.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS USER_TABLE(user_id INT)""")
con.commit()


@bot.message_handler(commands=['start', 'go'])
# @async_dec()
def ask(message):
    try:
        global markup_inline
        markup_inline = types.ReplyKeyboardMarkup(resize_keyboard=True)
        tab_look = types.KeyboardButton(text='Посмотреть курс валют')
        tab_remind = types.KeyboardButton(text='Вкл/выкл уведомления о курсе валют')

        markup_inline.add(tab_look, tab_remind)
        send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют\n"
        msg = bot.send_message(message.chat.id, send_message, reply_markup=markup_inline, parse_mode='html')
        # bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        # bot.register_next_step_handler(msg, answer)
        bot.register_next_step_handler(msg, answer)
    except Exception as e:
        print(e)
        msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
        bot.register_next_step_handler(msg, ask)


def answer(message):
    if message.text == 'Посмотреть курс валют':
        global gr_markup
        gr_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        grivna_button = types.KeyboardButton('Гривна')
        rubl_button = types.KeyboardButton('Рубль')
        back_to_start = types.KeyboardButton('Назад')
        gr_markup.add(grivna_button, rubl_button, back_to_start)
        msg = bot.send_message(message.chat.id, f'В <b>гривнах</b> или <b>рублях</b>?', reply_markup=gr_markup,
                               parse_mode='html')
        # bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id)
        bot.register_next_step_handler(msg, grivna_rubl)
    elif message.text == 'Вкл/выкл уведомления о курсе валют':
        global id
        global status
        id = message.from_user.id
        cursor.execute(f"""SELECT user_id FROM USER_TABLE WHERE user_id = {id}""")
        if cursor.fetchone() is None:
            try:
                cursor.execute(f"""INSERT INTO USER_TABLE VALUES(?)""", (id,))
                con.commit()
                msg = bot.send_message(id,
                                       'Уведомления о курсе доллара успешно подключены\nВремя: каждые 10 секунд')
                schedule.every().day.at("09:00").do(job)
                status = 1
                bot.register_next_step_handler(msg, answer)
            except Exception as e:
                print(e)
                bot.send_message(id, 'Не удалось подключить уведомления')
        else:
            try:
                cursor.execute(f"""DELETE FROM USER_TABLE WHERE user_id = {id}""")
                con.commit()
                msg = bot.send_message(id, 'Уведомления успешно отключены')
                schedule.cancel_job(job)
                status = 0
                bot.register_next_step_handler(msg, answer)
            except Exception as e:
                print(e)
                bot.send_message(id, 'Не удалось отключить уведомления')

        while status == 1:
            schedule.run_pending()
            sleep(1)


def job():
    # sqlite.cursor.execute(f"""SELECT user_id FROM USER_TABLE WHERE user_id = {id}""")
    # if sqlite.cursor.fetchone() is None:
    # return None
    # else:
    bot.send_message(id, f'<b>1</b> доллар США = <b>{str(convert_dollar[0].text)}</b> гривнам'
                                           f'\n<b>1</b> доллар США = <b>{str(convert_rus_dollar[0].text)}</b> рублям',
                     parse_mode='html')


@bot.message_handler(content_types=["text"])
def grivna_rubl(message):
    try:
        if message.text == 'Гривна':
            global markup_reply
            markup_reply = types.ReplyKeyboardMarkup()
            dollar = types.KeyboardButton('Курс доллара США')
            euro = types.KeyboardButton('Курс евро')
            pound = types.KeyboardButton('Курс фунта')
            rubl = types.KeyboardButton('Курс рубля')
            frank = types.KeyboardButton('Курс швейцарского франка')
            canadadollar = types.KeyboardButton('Курс канадского доллара')
            ausdollar = types.KeyboardButton('Курс австралийского доллара')
            yen = types.KeyboardButton('Курс японского йена')
            israel = types.KeyboardButton('Курс шекеля')
            zlotiy = types.KeyboardButton('Курс злотого')
            bitok = types.KeyboardButton('Криптовалюта...', )
            backtobutton = types.KeyboardButton('Назад')

            markup_reply.add(dollar, euro, pound, rubl, frank, canadadollar, ausdollar, yen, israel, zlotiy, bitok,
                             backtobutton)
            msg = bot.send_message(message.chat.id, f'<u>Выбери валюту:</u>', parse_mode='html',
                                   reply_markup=markup_reply)
            bot.register_next_step_handler(msg, kurs)
        elif message.text == 'Рубль':
            global rus_markup_reply
            rus_markup_reply = types.ReplyKeyboardMarkup()
            rus_dollar = types.KeyboardButton('Курс доллара США')
            rus_euro = types.KeyboardButton('Курс евро')
            rus_pound = types.KeyboardButton('Курс фунта')
            grivna = types.KeyboardButton('Курс гривны')
            rus_frank = types.KeyboardButton('Курс швейцарского франка')
            rus_canadadollar = types.KeyboardButton('Курс канадского доллара')
            rus_ausdollar = types.KeyboardButton('Курс австралийского доллара')
            rus_yen = types.KeyboardButton('Курс японского йена')
            rus_israel = types.KeyboardButton('Курс шекеля')
            rus_bitok = types.KeyboardButton('Криптовалюта...', )
            rus_backtobutton = types.KeyboardButton('Назад')

            rus_markup_reply.add(rus_dollar, rus_euro, rus_pound, grivna, rus_frank, rus_canadadollar, rus_ausdollar,
                                 rus_yen, rus_israel, rus_bitok, rus_backtobutton)
            msg = bot.send_message(message.chat.id, f'<u>Выбери валюту:</u>', parse_mode='html',
                                   reply_markup=rus_markup_reply)
            bot.register_next_step_handler(msg, rus_kurs)
        elif message.text == 'Назад':
            msg = bot.send_message(message.chat.id, 'Вы вернулись в начало', reply_markup=markup_inline)
            bot.register_next_step_handler(msg, answer)
        elif message.text == '/start':
            send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют"
            msg = bot.send_message(message.chat.id, send_message, parse_mode='html')
            bot.register_next_step_handler(msg, ask)
            # bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        else:
            msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
            bot.register_next_step_handler(msg, grivna_rubl)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неполадки с кодом :/')


def kurs(message):
    try:
        if message.text == 'Курс доллара США':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> доллар США = <b>{str(convert_dollar[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, kurs)
        elif message.text == 'Курс евро':
            msg = bot.send_message(message.chat.id, f'<b>1</b> евро = <b>{str(convert_euro[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, kurs)
        elif message.text == 'Курс фунта':
            msg = bot.send_message(message.chat.id, f'<b>1</b> фунт = <b>{str(convert_pound[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, kurs)
        elif message.text == 'Курс рубля':
            msg = bot.send_message(message.chat.id, f'<b>1</b> рубль = <b>{str(convert_rubl[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, kurs)
        elif message.text == 'Курс швейцарского франка':
            msg = bot.send_message(message.chat.id, f'<b>1</b> франк = <b>{str(convert_frank[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, kurs)
        elif message.text == 'Курс канадского доллара':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> канадский доллар = <b>{str(convert_canadadollar[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, kurs)
        elif message.text == 'Курс австралийского доллара':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> автралийский доллар = <b>{str(convert_ausdollar[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, kurs)
        elif message.text == 'Курс японского йена':
            msg = bot.send_message(message.chat.id, f'<b>1</b> йен = <b>{str(convert_yen[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, kurs)
        elif message.text == 'Курс шекеля':
            msg = bot.send_message(message.chat.id, f'<b>1</b> шекель = <b>{str(convert_israel[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, kurs)
        # elif message.text == 'Курс злотого':
        # msg = bot.send_message(message.chat.id, f'<b>1</b> шекель = <b>{str(convert_zlotiy[0].text)}</b> гривнам',
        # parse_mode='html')
        # bot.register_next_step_handler(msg, kurs)
        elif message.text == 'Криптовалюта...':
            global mark_up
            mark_up = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bitcoin = types.KeyboardButton('Курс Bitcoin')
            etherium = types.KeyboardButton('Курс Etherium')
            litecoin = types.KeyboardButton('Курс Litecoin')
            back_button = types.KeyboardButton('Назад')
            mark_up.add(bitcoin, etherium, litecoin, back_button)

            inline = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text='Узнать подробнее о криптовалютах...',
                                                    url='https://alpari.com/ru/beginner/glossary/cryptocurrency/')
            inline.add(url_button)

            msg = bot.send_message(message.chat.id, f'<b>Курс одних из самых популярных криптомонет в мире</b> :)',
                                   parse_mode='html', reply_markup=mark_up)
            bot.register_next_step_handler(msg, new_kurs)
            bot.send_message(message.chat.id, 'Хочешь узнать подробнее?🤔\nТогда жми сюда!', reply_markup=inline)
        elif message.text == 'Назад':
            msg = bot.send_message(message.chat.id, 'В гривнах или рублях?', reply_markup=gr_markup)
            bot.register_next_step_handler(msg, grivna_rubl)
        elif message.text == '/start':
            send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют"
            bot.send_message(message.chat.id, send_message, parse_mode='html')
            bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        else:
            msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
            bot.register_next_step_handler(msg, kurs)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неполадки с кодом :/')


def rus_kurs(message):
    try:
        if message.text == 'Курс доллара США':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> доллар США = <b>{str(convert_rus_dollar[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, rus_kurs)
        elif message.text == 'Курс евро':
            msg = bot.send_message(message.chat.id, f'<b>1</b> евро = <b>{str(convert_rus_euro[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, rus_kurs)
        elif message.text == 'Курс фунта':
            msg = bot.send_message(message.chat.id, f'<b>1</b> фунт = <b>{str(convert_rus_pound[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, rus_kurs)
        elif message.text == 'Курс гривны':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> гривна = <b>{str(convert_rus_grivna[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, rus_kurs)
        elif message.text == 'Курс швейцарского франка':
            msg = bot.send_message(message.chat.id, f'<b>1</b> франк = <b>{str(convert_rus_frank[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, rus_kurs)
        elif message.text == 'Курс канадского доллара':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> канадский доллар = <b>{str(convert_rus_canadadollar[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, rus_kurs)
        elif message.text == 'Курс австралийского доллара':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> автралийский доллар = <b>{str(convert_rus_ausdollar[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, rus_kurs)
        elif message.text == 'Курс японского йена':
            msg = bot.send_message(message.chat.id, f'<b>1</b> йен = <b>{str(convert_rus_yen[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, rus_kurs)
        elif message.text == 'Курс шекеля':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> шекель = <b>{str(convert_rus_israel[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, rus_kurs)
        elif message.text == 'Криптовалюта...':
            global rus_mark_up
            rus_mark_up = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bitcoin = types.KeyboardButton('Курс Bitcoin')
            etherium = types.KeyboardButton('Курс Etherium')
            litecoin = types.KeyboardButton('Курс Litecoin')
            back_button = types.KeyboardButton('Назад')
            rus_mark_up.add(bitcoin, etherium, litecoin, back_button)

            inline = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text='Узнать подробнее о криптовалютах...',
                                                    url='https://alpari.com/ru/beginner/glossary/cryptocurrency/')
            inline.add(url_button)

            msg = bot.send_message(message.chat.id, f'<b>Курс одних из самых популярных криптомонет в мире</b> :)',
                                   parse_mode='html', reply_markup=rus_mark_up)
            bot.register_next_step_handler(msg, new_rus_kurs)
            bot.send_message(message.chat.id, 'Хочешь узнать подробнее?🤔\nТогда жми сюда!', reply_markup=inline)
        elif message.text == 'Назад':
            msg = bot.send_message(message.chat.id, 'В гривнах или рублях?', reply_markup=gr_markup)
            bot.register_next_step_handler(msg, grivna_rubl)
        elif message.text == '/start':
            send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют"
            bot.send_message(message.chat.id, send_message, parse_mode='html')
            bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        else:
            msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
            bot.register_next_step_handler(msg, rus_kurs)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неполадки с кодом :/')


def new_kurs(message):
    try:
        reply_question = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        dollar_question = types.KeyboardButton('В долларах')
        euro_question = types.KeyboardButton('В евро')
        grivna_question = types.KeyboardButton('В гривнах')
        back_but = types.KeyboardButton('Назад')
        reply_question.add(dollar_question, euro_question, grivna_question, back_but)

        if message.text == 'Курс Bitcoin':
            msg = bot.send_message(message.chat.id, f'<b>В какой валюте?</b>', parse_mode='html',
                                   reply_markup=reply_question)
            bot.register_next_step_handler(msg, dollar_grivna_bitcoin)
        elif message.text == 'Курс Etherium':
            msg = bot.send_message(message.chat.id, f'<b>В какой валюте?</b>', parse_mode='html',
                                   reply_markup=reply_question)
            bot.register_next_step_handler(msg, dollar_grivna_ether)
        elif message.text == 'Курс Litecoin':
            msg = bot.send_message(message.chat.id, f'<b>В какой валюте?</b>', parse_mode='html',
                                   reply_markup=reply_question)
            bot.register_next_step_handler(msg, dollar_grivna_litecoin)
        elif message.text == 'Назад':
            msg = bot.send_message(message.chat.id, f'<u>Выбери валюту:</u>', parse_mode='html',
                                   reply_markup=markup_reply)
            bot.register_next_step_handler(msg, kurs)
        elif message.text == '/start':
            send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют"
            bot.send_message(message.chat.id, send_message, parse_mode='html')
            bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        else:
            msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
            bot.register_next_step_handler(msg, new_kurs)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неполадки с кодом :/')


def new_rus_kurs(message):
    try:
        rus_reply_question = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        dollar_question = types.KeyboardButton('В долларах')
        rus_question = types.KeyboardButton('В рублях')
        euro_question = types.KeyboardButton('В евро')
        back_but = types.KeyboardButton('Назад')
        rus_reply_question.add(dollar_question, euro_question, rus_question, back_but)

        if message.text == 'Курс Bitcoin':
            msg = bot.send_message(message.chat.id, f'<b>В какой валюте?</b>', parse_mode='html',
                                   reply_markup=rus_reply_question)
            bot.register_next_step_handler(msg, dollar_rus_bitcoin)
        elif message.text == 'Курс Etherium':
            msg = bot.send_message(message.chat.id, f'<b>В какой валюте?</b>', parse_mode='html',
                                   reply_markup=rus_reply_question)
            bot.register_next_step_handler(msg, dollar_rus_ether)
        elif message.text == 'Курс Litecoin':
            msg = bot.send_message(message.chat.id, f'<b>В какой валюте?</b>', parse_mode='html',
                                   reply_markup=rus_reply_question)
            bot.register_next_step_handler(msg, dollar_rus_litecoin)
        elif message.text == 'Назад':
            msg = bot.send_message(message.chat.id, f'<u>Выбери валюту:</u>', parse_mode='html',
                                   reply_markup=rus_markup_reply)
            bot.register_next_step_handler(msg, rus_kurs)
        elif message.text == '/start':
            send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют"
            bot.send_message(message.chat.id, send_message, parse_mode='html')
            bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        else:
            msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
            bot.register_next_step_handler(msg, new_rus_kurs)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неполадки с кодом :/')


def dollar_grivna_bitcoin(message):
    try:
        if message.text == 'В долларах':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Bitcoin = <b>{str(convert_bitcoin_dollar[0].text)}</b> долларам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_grivna_bitcoin)
        elif message.text == 'В евро':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Bitcoin = <b>{str(convert_bitcoin_euro[0].text)}</b> евро',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_grivna_bitcoin)
        elif message.text == 'В гривнах':
            msg = bot.send_message(message.chat.id, f'<b>1</b> Bitcoin = <b>{str(convert_bitcoin[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_grivna_bitcoin)
        elif message.text == 'Назад':
            msg = bot.send_message(message.chat.id, f'<u>Ты вернулся назад</u>', reply_markup=mark_up,
                                   parse_mode='html')
            bot.register_next_step_handler(msg, new_kurs)
        elif message.text == '/start':
            send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют"
            bot.send_message(message.chat.id, send_message, parse_mode='html')
            bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        else:
            msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
            bot.register_next_step_handler(msg, dollar_grivna_bitcoin)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неполадки с кодом :/')


def dollar_rus_bitcoin(message):
    try:
        if message.text == 'В долларах':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Bitcoin = <b>{str(convert_bitcoin_dollar[0].text)}</b> долларам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_rus_bitcoin)
        elif message.text == 'В евро':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Bitcoin = <b>{str(convert_bitcoin_euro[0].text)}</b> евро',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_rus_bitcoin)
        elif message.text == 'В рублях':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Bitcoin = <b>{str(convert_rus_bitcoin[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_rus_bitcoin)
        elif message.text == 'Назад':
            msg = bot.send_message(message.chat.id, f'<u>Ты вернулся назад</u>', reply_markup=rus_mark_up,
                                   parse_mode='html')
            bot.register_next_step_handler(msg, new_rus_kurs)
        elif message.text == '/start':
            send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют"
            bot.send_message(message.chat.id, send_message, parse_mode='html')
            bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        else:
            msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
            bot.register_next_step_handler(msg, dollar_rus_bitcoin)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неполадки с кодом :/')


def dollar_grivna_ether(message):
    try:
        if message.text == 'В долларах':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Etherium = <b>{str(convert_ether_dollar[0].text)}</b> долларам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_grivna_ether)
        elif message.text == 'В евро':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Etherium = <b>{str(convert_ether_euro[0].text)}</b> евро',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_grivna_ether)
        elif message.text == 'В гривнах':
            msg = bot.send_message(message.chat.id, f'<b>1</b> Etherium = <b>{str(convert_ether[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_grivna_ether)
        elif message.text == 'Назад':
            msg = bot.send_message(message.chat.id, f'<u>Ты вернулся назад</u>', reply_markup=mark_up,
                                   parse_mode='html')
            bot.register_next_step_handler(msg, new_kurs)
        elif message.text == '/start':
            send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют"
            bot.send_message(message.chat.id, send_message, parse_mode='html')
            bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        else:
            msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
            bot.register_next_step_handler(msg, dollar_grivna_ether)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неполадки с кодом :/')


def dollar_rus_ether(message):
    try:
        if message.text == 'В долларах':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Etherium = <b>{str(convert_ether_dollar[0].text)}</b> долларам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_rus_ether)
        elif message.text == 'В евро':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Etherium = <b>{str(convert_ether_euro[0].text)}</b> евро',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_rus_ether)
        elif message.text == 'В рублях':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Etherium = <b>{str(convert_rus_ether[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_rus_ether)
        elif message.text == 'Назад':
            msg = bot.send_message(message.chat.id, f'<u>Ты вернулся назад</u>', reply_markup=rus_mark_up,
                                   parse_mode='html')
            bot.register_next_step_handler(msg, new_rus_kurs)
        elif message.text == '/start':
            send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют"
            bot.send_message(message.chat.id, send_message, parse_mode='html')
            bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        else:
            msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
            bot.register_next_step_handler(msg, dollar_rus_ether)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неполадки с кодом :/')


def dollar_grivna_litecoin(message):
    try:
        if message.text == 'В долларах':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Litecoin = <b>{str(convert_litecoin_dollar[0].text)}</b> долларам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_grivna_litecoin)
        elif message.text == 'В евро':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Litecoin = <b>{str(convert_litecoin_euro[0].text)}</b> евро',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_grivna_litecoin)
        elif message.text == 'В гривнах':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Litecoin = <b>{str(convert_litecoin[0].text)}</b> гривнам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_grivna_litecoin)
        elif message.text == 'Назад':
            msg = bot.send_message(message.chat.id, f'<u>Ты вернулся назад</u>', reply_markup=mark_up,
                                   parse_mode='html')
            bot.register_next_step_handler(msg, new_kurs)
        elif message.text == '/start':
            send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют"
            bot.send_message(message.chat.id, send_message, parse_mode='html')
            bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        else:
            msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
            bot.register_next_step_handler(msg, dollar_grivna_litecoin)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неполадки с кодом :/')


def dollar_rus_litecoin(message):
    try:
        if message.text == 'В долларах':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Litecoin = <b>{str(convert_litecoin_dollar[0].text)}</b> долларам',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_rus_litecoin)
        elif message.text == 'В евро':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Litecoin = <b>{str(convert_litecoin_euro[0].text)}</b> евро',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_rus_litecoin)
        elif message.text == 'В рублях':
            msg = bot.send_message(message.chat.id,
                                   f'<b>1</b> Litecoin = <b>{str(convert_rus_litecoin[0].text)}</b> рублям',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, dollar_rus_litecoin)
        elif message.text == 'Назад':
            msg = bot.send_message(message.chat.id, f'<u>Ты вернулся назад</u>', reply_markup=rus_mark_up,
                                   parse_mode='html')
            bot.register_next_step_handler(msg, new_rus_kurs)
        elif message.text == '/start':
            send_message = f"Здравствуй, <b>{message.from_user.first_name}</b>\nЯ могу показать тебе курс известных мировых валют"
            bot.send_message(message.chat.id, send_message, parse_mode='html')
            bot.send_message(message.chat.id, 'Желаешь узнать курс?😏', reply_markup=markup_inline)
        else:
            msg = bot.send_message(message.chat.id, 'Я не знаю, что ответить...')
            bot.register_next_step_handler(msg, dollar_rus_litecoin)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неполадки с кодом :/')


'''def schedule_checker(message):
    cursor.execute(f"""SELECT user_id FROM USER_TABLE WHERE user_id = {id}""")
    if cursor.fetchone() is None:
        schedule.cancel_job(lambda: job(message))
    else:
        schedule.every(10).seconds.do(lambda: job(message))
    while True:
        schedule.run_pending()
        sleep(1)'''

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
