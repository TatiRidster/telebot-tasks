from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import os
from controllers import *


def tasks_bot(token):
    bot = Bot(token)
    updater = Updater(token)
    dispatcher = updater.dispatcher
    print('Бот работает...')

    def start(update, context):
        arg = context.args
        keyboard = ReplyKeyboardMarkup([], resize_keyboard=True)
        item_1 = KeyboardButton('Посмотреть')
        item_2 = KeyboardButton('Добавить')
        item_3 = KeyboardButton('Изменить')
        item_4 = KeyboardButton('Удалить')
        keyboard.keyboard.append([item_1,item_2,item_3,item_4])
        if not arg:
            context.bot.send_message(update.effective_chat.id, "Привет", reply_markup=keyboard)
        else:
            context.bot.send_message(update.effective_chat.id, f"{' '.join(arg)}")


    def info(update, context):
        context.bot.send_message(update.effective_chat.id, "Меня создала Группа 3")

    def message(update, context):
        text = update.message.text
        if text.lower() == 'привет':
            context.bot.send_message(update.effective_chat.id, 'И тебе привет..')
        elif text.lower() == 'посмотреть':
            context.bot.send_message(update.effective_chat.id, f'{get_tasks}')
        elif text.lower() == 'добавить':
            context.bot.send_message(update.effective_chat.id, f'{get_tasks}')
            # TODO: conversation handler
        else:
            context.bot.send_message(update.effective_chat.id, 'я тебя не понимаю')

    def unknown(update, context):
        context.bot.send_message(update.effective_chat.id, f'Шо сказал, не пойму')

    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info)
    message_handler = MessageHandler(Filters.text, message)
    unknown_handler = MessageHandler(Filters.command, unknown)  # /game

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


def main():
    tasks_bot(os.getenv('TOKEN'))


if __name__ == "__main__":
    main()
