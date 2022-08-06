from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import os


def tasks_bot(token):
    bot = Bot(token)
    updater = Updater(token)
    dispatcher = updater.dispatcher
    print('server started')

    updater.start_polling()
    updater.idle()


def main():
    tasks_bot(os.getenv('TOKEN'))


if __name__ == "__main__":
    main()
