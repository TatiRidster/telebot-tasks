from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
import os
from controllers import *


task_id, task_name, task_status = range(3)


def tasks_bot(token):
    bot = Bot(token)
    updater = Updater(token)
    dispatcher = updater.dispatcher
    print('Бот работает...')

    def start(update, context):
        arg = context.args
        keyboard = ReplyKeyboardMarkup([
            [KeyboardButton('Посмотреть все'), KeyboardButton('Посмотреть готовые'), KeyboardButton('Посмотреть в работе')],
            [KeyboardButton('Добавить'), KeyboardButton('Изменить'), KeyboardButton('Удалить')],
            [KeyboardButton('Сохранить изменения')]
        ], resize_keyboard=True)

        # keyboard.keyboard.append([item_1,item_2,item_3,item_4])
        if not arg:
            context.bot.send_message(update.effective_chat.id, "Привет", reply_markup=keyboard)
        else:
            context.bot.send_message(update.effective_chat.id, f"{' '.join(arg)}")


    def info(update, context):
        context.bot.send_message(update.effective_chat.id, "Меня создала Группа 3 потока февраль'22")

    def message(update, context):
        text = update.message.text
        if text.lower() == 'привет':
            context.bot.send_message(update.effective_chat.id, 'И тебе привет..')
        elif text.lower()== 'посмотреть все':
            context.bot.send_message(update.effective_chat.id, f'{get_tasks_1}')
        elif text.lower() == 'посмотреть готовые':
            context.bot.send_message(update.effective_chat.id, f'{get_tasks_2}_2')
        elif text.lower() == 'посмотреть в работе':
            context.bot.send_message(update.effective_chat.id, f'{get_tasks_3}_3')
        elif text.lower()== 'добавить':
            context.bot.send_message(update.effective_chat.id, 'Введите задачу:')
            # arg=context.args
            # new_tasks= add_task(all_task,arg=arg)
            # context.bot.send_message(update.effective_chat.id, f'{new_tasks}')
        else:
            context.bot.send_message(update.effective_chat.id, 'я тебя не понимаю')
        return update.message.text


    def stop(update, context):
        context.message.send_message(update.effective_chat.id, "Хорошего дня!")
        return ConversationHandler.END


    def unknown(update, context):
        context.bot.send_message(update.effective_chat.id, f'Шо сказал, не пойму')


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            task_id: [],
            task_name: [],
            task_status: []
        },
        fallbacks=[CommandHandler('stop', stop)]
    )


    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info)
    stop_handler = CommandHandler('stop', stop)
    message_handler = MessageHandler(Filters.text, message)
    unknown_handler = MessageHandler(Filters.command, unknown)  # /game

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(stop_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


def main():
    tasks_bot(os.getenv('TOKEN'))
    print('Бот остановлен!')


if __name__ == "__main__":
    main()
