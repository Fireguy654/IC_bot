from telegram import ReplyKeyboardMarkup

KEYBOARD = [["/start", "/help"], ["/create_meme"]]


def start(update, context):
    update.message.reply_text('hello',
                              reply_markup=ReplyKeyboardMarkup(KEYBOARD, one_time_keyboard=True))
