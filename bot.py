import telebot
from threading import Thread
from telebot import types
from mainmain import *
import logging
import schedule


bot = telebot.TeleBot(TOKEN)

logging.basicConfig(filename=LOG_FILE, filemode='a', level=logging.DEBUG,
                    format='%(asctime)s,%(msecs)d %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = telebot.logging.getLogger(__name__)


def sheduler():
    schedule.every().day.at("12:00").do(daily_notify)
    # schedule.every(15).seconds.do(daily_notify)
    while True:
        schedule.run_pending()
        sleep(1)


def daily_notify():
    daily_query = 'SELECT user_id FROM users WHERE notify="YES";'
    result_daily_query = post_sql_query(daily_query)
    if result_daily_query:
        users = list(map(lambda x: x[0], result_daily_query))
        currency_msg = get_currency()
        for user in users:
            for msg in currency_msg:
                bot.send_message(chat_id=user, text=msg)


def get_currency():
    query_cur = f'SELECT USD, CAD, AUD, EUR, GBP, CHF, JPY, ILS, PLN, UAH, BITCOIN ' \
                f'FROM currency_rub ORDER BY id DESC LIMIT 1;'
    currency = post_sql_query(query_cur)
    result_currency = list(zip(list(COUNTRY_CODE.keys()), currency[0]))
    text_to_send = [f'{COUNTRY_CODE[i[0]]} = {i[1]} {MAIN_CURRENCY}' for i in result_currency]
    return text_to_send


@bot.message_handler(commands=['notify'])
def add(message):
    sql_check_id = f"SELECT * FROM users WHERE user_id = {message.from_user.id}"
    result_check_id = post_sql_query(sql_check_id)
    print(result_check_id)
    if not result_check_id:
        notify = 'YES'
        sql_reg_user = f'INSERT OR IGNORE INTO users (user_id, username, reg_date, notify) ' \
                       f'VALUES ({message.from_user.id},"{message.from_user.username}", ' \
                       f'"{datetime.today().strftime("%Y.%m.%d %H:%M:%S")}", "{notify}");'
        post_sql_query(sql_reg_user)
        bot.send_message(message.from_user.id, 'Автоматические уведомления включены\nЕжедневно в 12:00')
    else:
        user_id, *tmp, notify = result_check_id[0]
        print(user_id, *tmp, notify, sep='|')
        if result_check_id and notify == 'NO':
            notify = 'YES'
            sql_upd_user = f'UPDATE users SET notify = "{notify}" WHERE user_id = {user_id};'
            post_sql_query(sql_upd_user)
            bot.send_message(user_id, 'Автоматические уведомления включены\nЕжедневно в 12:00')
        else:
            notify = 'NO'
            sql_upd_user = f'UPDATE users SET notify = "{notify}" WHERE user_id = {user_id};'
            post_sql_query(sql_upd_user)
            bot.send_message(user_id, 'Автоматические уведомления отключены')


@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message: True, content_types=['text'])
def main_menu(message):
    show_button = types.InlineKeyboardButton(text="Show Currency", callback_data="Show")
    keyboardmain = types.InlineKeyboardMarkup()
    keyboardmain.add(show_button)
    try:
        bot.send_message(message.from_user.id, HELP, reply_markup=keyboardmain)
    except telebot.apihelper.ApiException:
        logging.exception(f'Send Notification ERROR - {telebot.apihelper.ApiException}')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "Show":
        currency_msg = get_currency()
        for msg in currency_msg:
            try:
                bot.send_message(chat_id=call.message.chat.id, text=msg)
            except telebot.apihelper.ApiException:
                logging.exception(f'Send Notification ERROR - {telebot.apihelper.ApiException}')
        sleep(1)
        show_button = types.InlineKeyboardButton(text="Show Currency", callback_data="Show")
        keyboardmain = types.InlineKeyboardMarkup()
        keyboardmain.add(show_button)
        try:
            bot.send_message(chat_id=call.message.chat.id, text=WELCOME, reply_markup=keyboardmain)
        except telebot.apihelper.ApiException:
            logging.exception(f'Send Notification ERROR - {telebot.apihelper.ApiException}')


if __name__ == "__main__":
    Thread(target=sheduler, args=()).start()
    Thread(target=main_body, args=()).start()
    try:
        bot.polling(none_stop=True)
    except Exception as Error:
        logging.exception(f'Polling error - {Error}')
