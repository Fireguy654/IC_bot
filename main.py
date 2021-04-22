from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler

from Functions import start, gif_send
from info import TOKEN


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start.start))
    dp.add_handler(CommandHandler('gif', gif_send.send_gif))
    dp.add_handler(CommandHandler('gifn', gif_send.send_some_gifs))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
