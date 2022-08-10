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
    def edit_id(update, _):
        update.message.reply_text('Введите ID задачи, которую вы хотите изменить:')
        return ID
    
    
    def eenter_task(update, _):
        global temp_id
        temp_id = int(update.message.text)
        update.message.reply_text('Введите изменения в задачу:')
        return TASK

    def edit_t(update, _):
        global temp_task
        temp_task = update.message.text
        update.message.reply_text('Введите статус задачи: 1 - выполнено, 0 - не выполнено')
        return IS_DONE

    def edit_f(update, _):
        temp_flag = update.message.text
        for k, v in all_task.items():
            if temp_id == k:
                v['task'] = temp_task
                v['is_done'] = temp_flag
        print(temp_task,temp_flag)
        update.message.reply_text('Задача изменена')
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
        elif text.lower() == 'изменить': 
            context.bot.send_message(update.effective_chat.id, f'{print_todo(all_task, 1)}')
        elif text.lower() == 'сохранить изменения':
            context.bot.send_message(update.effective_chat.id, f'{save_data(all_task)}')
        elif text.lower() == 'удалить':
            context.bot.send_message(update.effective_chat.id, f'{print_todo(all_task, 1)}')
            context.bot.send_message(update.effective_chat.id, 'Введите ID задачи для удаления:')
            #context.bot.send_message(update.effective_chat.id, f'{del_task(all_task, ID)}')
            return ID
        else:
            context.bot.send_message(update.effective_chat.id, f'я тебя не понимаю')
            context.bot.send_sticker(update.effective_chat.id,
                                     'CAACAgIAAxkBAAEFhIdi80CHP1R-bh96JlfoSeNBmq1lqQACIhMAAl1scEuuLYe9O-OAPikE')
            # gif = open('src/bender_unknown.gif', 'rb')
            # context.bot.send_video(update.effective_chat.id, video=gif)
            # gif.close()
        return update.message.text

    def add(update, _):
        update.message.reply_text('Введите дело, которое вы хотите добавить или /cancel, чтобы не добавлять')
        return TASK
    def delete(update, _):
        update.message.reply_text('Введите ID задачи, которую вы хотите удалить:')
        return ID
    def delete_task(update, context):
        #update.message.reply_text('Введите ID задачи, которую вы хотите удалить, или /cancel, чтобы не удалять')
        update.message.reply_text(del_task(all_task, update.message.text))
        context.bot.send_sticker(update.effective_chat.id,
                                 'CAACAgIAAxkBAAEFhIFi80Anl4Ls15nv7g5HF7m-AkZVpQACfRMAAqN3qEvCWDsDiG_N4CkE')
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
            # ID:
            TASK: [MessageHandler(Filters.text, enter_task)]
            # IS_DONE:
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    conv_handler2 = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(удалить|Удалить)$'), delete)],
        states={
            ID: [MessageHandler(Filters.text, delete_task)]
            #TASK: 
            # IS_DONE:
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    conv_handler3 = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(изменить|Изменить)$'), edit_id)],
        states={
            ID: [MessageHandler(Filters.text, eenter_task)],
            TASK: [MessageHandler(Filters.text, edit_t)],
            IS_DONE: [MessageHandler(Filters.text, edit_f)]
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
    edit_id_handler = CommandHandler('edit_id', edit_id)
    eenter_task_handler = CommandHandler('eenter_task', eenter_task)
    edit_f_handler = CommandHandler('edit_f', edit_f)
    edit_t_handler = CommandHandler('edit_t', edit_t)

    message_handler = MessageHandler(Filters.text, message)
    unknown_handler = MessageHandler(Filters.command, unknown)  # /game

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(stop_handler)
    dispatcher.add_handler(new_rask_handler)
    dispatcher.add_handler(enter_task_handler)
    dispatcher.add_handler(conv_handler2)
    dispatcher.add_handler(conv_handler3)
    dispatcher.add_handler(cancel_handler)
    dispatcher.add_handler(delete_task_handler)
    dispatcher.add_handler(delete_task_id_handler)
    dispatcher.add_handler(edit_id_handler)
    dispatcher.add_handler(eenter_task_handler)
    dispatcher.add_handler(edit_f_handler)
    dispatcher.add_handler(edit_t_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()


def main():
    tasks_bot(os.getenv('TOKEN'))
    print('Бот остановлен!')


if __name__ == "__main__":
    main()
