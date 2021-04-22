from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler

from Functions import start, meme_generator
from info import TOKEN


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    meme_handler = ConversationHandler(
        entry_points=[CommandHandler('create_meme', meme_generator.create_meme_processing)],
        states={
            1: [MessageHandler(Filters.all, meme_generator.get_meme_text)],
            2: [MessageHandler(Filters.all, meme_generator.get_meme_photo)]
        },
        fallbacks=[CommandHandler('stop', meme_generator.stop)])
    dp.add_handler(meme_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
