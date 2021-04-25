from telegram import ReplyKeyboardMarkup

KEYBOARD = [["/something"],
            ["/ch_study_mode", "/ch_answer_mode"],
            ["/gif", "/create_meme"]]

HELP_TEXT = 'Введите "/something", чтобы я сгенерировал вам предложение,\n' + \
    '"/ch_study_mode", если хотите изменить режим обучения меня,\n' + \
    '"/ch_answer_mode", если хотите включить/отключить режим автоответа.\n' + \
    'При вызове "/gif <тема>", я отправлю вам тематическую гифку,\n' + \
    'при наборе "/gifn <тема> <количество гифок>", будет отправлен набор гифок заданного количества.\n' + \
    'Если вы захотите сделать мем, можете просто набрать "/create_meme [текст]".\n' + \
    'При вызове "/get_image <тема>" вы получите от меня изображение на указанную тему,\n' + \
    'при наборе "/getn_images <количество> <тема>" вы получите несколько таких картинок."\n' + \
    'При наборе "/get_music <количество> <название>" вы получите несколько популярных треков по заданному названию.'


def get_help(update, context):
    update.message.reply_text(HELP_TEXT, reply_markup=ReplyKeyboardMarkup(KEYBOARD,
                                                                          one_time_keyboard=True))
