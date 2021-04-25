from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler

from Functions import start, get_info, send_text, AI_mods, help
from Functions import meme_generator, gif_send
from info import TOKEN


# main - функция, вызываемая при запуске программы.
# Связывает сигналы полученные от бота с их обработчиками, подключая их из директории Functions.
# Запускает бесконечный цикл обработки сигналов.
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start.start))
    dp.add_handler(CommandHandler("help", help.get_help))

    dp.add_handler(CommandHandler("gif", gif_send.send_gif))
    dp.add_handler(CommandHandler("gifn", gif_send.send_some_gifs))

    dp.add_handler(CommandHandler("something", send_text.send_message))
    dp.add_handler(CommandHandler("ch_study_mode", AI_mods.ch_study_mode))
    dp.add_handler(CommandHandler("ch_answer_mode", AI_mods.ch_ans_mode))
    meme_handler = ConversationHandler(
        entry_points=[CommandHandler("create_meme", meme_generator.create_meme_processing)],
        states={1: [MessageHandler(Filters.all, meme_generator.get_meme_text)],
                2: [MessageHandler(Filters.all, meme_generator.get_meme_photo)]},
        fallbacks=[CommandHandler("stop", meme_generator.stop)])
    dp.add_handler(meme_handler)
    dp.add_handler(MessageHandler(Filters.text, get_info.get_info))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
