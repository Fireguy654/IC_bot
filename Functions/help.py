from telegram import ReplyKeyboardMarkup

KEYBOARD = [["/something"],
            ["/ch_study_mode", "/ch_answer_mode"],
            ["/gif", "/create_meme"]]

HELP_TEXT = 'Введите "/something", чтобы я сгенерировал вам предложение, ' + \
    '"/ch_study_mode", если хотите изменить режим обучения меня, ' + \
    '"/ch_answer_mode", если хотите включить/отключить режим автоответа.\n' + \
    'При вызове "/gif <тема>", я отправлю вам тематическую гифку, ' + \
    'при наборе "/gifn <тема> <количество гифок>", будет отправлен набор гифок заданного количества.\n' + \
    'Если вы захотите сделать мем, можете просто набрать "/create_meme [текст]".'


def get_help(update, context):
    update.message.reply_text(HELP_TEXT, reply_markup=ReplyKeyboardMarkup(KEYBOARD,
                                                                          one_time_keyboard=True))
