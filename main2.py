import schedule
import telebot
from threading import Thread
from time import sleep

TOKEN = "Some Token"

bot = telebot.TeleBot('1132614441:AAHHFesKOJsuZhRGI1STgPgIBrktGR1E0aM')
id = 346457069 # This is our chat id.

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

def function_to_run():
    return bot.send_message(id, "This is a message to send.")

if __name__ == "__main__":
    # Create the job in schedule.
    schedule.every().days.at("13:34").do(function_to_run)

    # Spin up a thread to run the schedule check so it doesn't block your bot.
    # This will take the function schedule_checker which will check every second
    # to see if the scheduled job needs to be ran.
    Thread(target=schedule_checker).start()

    # And then of course, start your server.
    bot.polling(none_stop=True, interval=0)