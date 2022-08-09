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

    def enter_task(update, _):
        update.message.reply_text(add_task(all_task, update.message.text))
        # todo_new = update.message.text
        # if todo_new:
        #     id_new = max(list(x for x in all_task.keys())) + 1
        #     result_new = {
        #         'task': todo_new,
        #         'is_done': 0
        #     }
        #     all_task[id_new] = result_new
        #     update.message.reply_text(f"Задача '{todo_new}' добавлена.")
        # else:
        #     update.message.reply_text('Название не может быть пустым')
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
        else:
            context.bot.send_message(update.effective_chat.id, 'я тебя не понимаю')
        return update.message.text

    def add(update, _):
        update.message.reply_text('Введите дело, которое вы хотите добавить или /cancel, чтобы не добавлять')
        return TASK

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
            # ID:
            TASK: [MessageHandler(Filters.text, enter_task)]
            # IS_DONE:
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info)
    stop_handler = CommandHandler('stop', stop)
    new_rask_handler = CommandHandler('add', add)
    enter_task_handler = CommandHandler('enter_task', enter_task)
    cancel_handler = CommandHandler('cancel', cancel)
    message_handler = MessageHandler(Filters.text, message)
    unknown_handler = MessageHandler(Filters.command, unknown)  # /game

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(stop_handler)
    dispatcher.add_handler(new_rask_handler)
    dispatcher.add_handler(enter_task_handler)
    dispatcher.add_handler(cancel_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()


def main():
    tasks_bot(os.getenv('TOKEN'))
    print('Бот остановлен!')


if __name__ == "__main__":
    main()
