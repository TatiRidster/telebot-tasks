from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
import os
from controllers import *

ID = 'id'
TASK = 'task'
IS_DONE = 'is_done'

keyboard = ReplyKeyboardMarkup([
    [KeyboardButton('Посмотреть все'),
     KeyboardButton('Посмотреть готовые'),
     KeyboardButton('Посмотреть в работе')],

    [KeyboardButton('Добавить'),
     KeyboardButton('Изменить'),
     KeyboardButton('Удалить')],

    [KeyboardButton('Сохранить изменения')]
], resize_keyboard=True)


def tasks_bot(token):
    bot = Bot(token)
    updater = Updater(token)
    dispatcher = updater.dispatcher
    print('Бот работает...')

    def start(update, context):
        arg = context.args
        if not arg:
            context.bot.send_message(update.effective_chat.id, "Привет", reply_markup=keyboard)
        else:
            context.bot.send_message(update.effective_chat.id, f"{' '.join(arg)}")

    def info(update, context):
        context.bot.send_message(update.effective_chat.id, "Меня создала Группа 3 потока февраль'22")

    def enter_task(update, context):
        update.message.reply_text(add_task(all_task, update.message.text))
        context.bot.send_sticker(update.effective_chat.id,
                                 'CAACAgIAAxkBAAEFhIFi80Anl4Ls15nv7g5HF7m-AkZVpQACfRMAAqN3qEvCWDsDiG_N4CkE')
        return ConversationHandler.END

    def message(update, context):
        text = update.message.text
        if text.lower() == 'привет':
            context.bot.send_message(update.effective_chat.id, 'И тебе привет..')
        elif text.lower() == 'посмотреть все':
            context.bot.send_message(update.effective_chat.id, f'{print_todo(all_task, 1)}')
        elif text.lower() == 'посмотреть готовые':
            context.bot.send_message(update.effective_chat.id, f'{print_todo(all_task, 2)}')
        elif text.lower() == 'посмотреть в работе':
            context.bot.send_message(update.effective_chat.id, f'{print_todo(all_task, 3)}')
        elif text.lower() == 'добавить':
            context.bot.send_message(update.effective_chat.id, 'Введите задачу:')
            return TASK
        elif text.lower() == 'сохранить изменения':
            context.bot.send_message(update.effective_chat.id, f'{save_data(all_task)}')
            context.bot.send_sticker(update.effective_chat.id,
                                     'CAACAgIAAxkBAAEFhYdi88Hlg7HNkhZrCUxW_p3Eg1ONBQACgRUAAuvgUUgNpYhAo6mJJykE')
        elif text.lower() == 'удалить':
            context.bot.send_message(update.effective_chat.id, f'{print_todo(all_task, 1)}')
            context.bot.send_message(update.effective_chat.id, 'Введите ID задачи для удаления:')
            return ID
        else:
            context.bot.send_message(update.effective_chat.id, f'я тебя не понимаю')
            context.bot.send_sticker(update.effective_chat.id,
                                     'CAACAgIAAxkBAAEFhIdi80CHP1R-bh96JlfoSeNBmq1lqQACIhMAAl1scEuuLYe9O-OAPikE')
        return update.message.text

    def add(update, _):
        update.message.reply_text('Введите дело, которое вы хотите добавить')
        return TASK

    def delete(update, _):
        update.message.reply_text('Введите ID задачи, которую вы хотите удалить:')
        return ID

    def delete_task(update, context):
        update.message.reply_text(del_task(all_task, update.message.text))
        context.bot.send_sticker(update.effective_chat.id,
                                 'CAACAgIAAxkBAAEFhX1i88Af-40yVf9rWSrtJt40epxGRgACjwMAAkcVaAlna9Kp-go6HCkE')
        return ConversationHandler.END

    def cancel(update, _):
        update.message.reply_text('Хорошо, не добавляем')
        return ConversationHandler.END

    def stop(update, context):
        context.message.send_message(update.effective_chat.id, "Хорошего дня!")

    def unknown(update, context):
        context.bot.send_message(update.effective_chat.id, f'Шо сказал, не пойму')

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(добавить|Добавить)$'), add)],
        states={
            TASK: [MessageHandler(Filters.text, enter_task)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    conv_handler2 = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(удалить|Удалить)$'), delete)],
        states={
            ID: [MessageHandler(Filters.text, delete_task)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info)
    stop_handler = CommandHandler('stop', stop)
    new_rask_handler = CommandHandler('add', add)
    enter_task_handler = CommandHandler('enter_task', enter_task)
    cancel_handler = CommandHandler('cancel', cancel)
    delete_task_handler = CommandHandler('delete', delete)
    delete_task_id_handler = CommandHandler('delete_task', delete_task)
    message_handler = MessageHandler(Filters.text, message)
    unknown_handler = MessageHandler(Filters.command, unknown)  # /game

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(stop_handler)
    dispatcher.add_handler(new_rask_handler)
    dispatcher.add_handler(enter_task_handler)
    dispatcher.add_handler(conv_handler2)
    dispatcher.add_handler(cancel_handler)
    dispatcher.add_handler(delete_task_handler)
    dispatcher.add_handler(delete_task_id_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()


def main():
    tasks_bot(os.getenv('TOKEN'))
    print('Бот остановлен!')


if __name__ == "__main__":
    main()
