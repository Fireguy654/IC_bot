from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler

from Functions import start, get_info, send_text, AI_mods
from info import TOKEN


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start.start))
    dp.add_handler(CommandHandler("something", send_text.send_message))
    dp.add_handler(CommandHandler("ch_study_mode", AI_mods.ch_study_mode))
    dp.add_handler(CommandHandler("ch_answer_mode", AI_mods.ch_ans_mode))
    dp.add_handler(MessageHandler(Filters.text, get_info.get_info))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
