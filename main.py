import telebot
import os


def tasks_bot(token):
    bot = telebot.TeleBot(token)

    bot.polling()


def main():
    tasks_bot(os.getenv('TOKEN'))


if __name__ == "__main__":
    main()
