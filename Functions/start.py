from telegram import ReplyKeyboardMarkup

KEYBOARD = [["/help"]]


def start(update, context):
    update.message.reply_text('Привет, пользователь!\n' +
                              'Я готов предоставить тебе несколько полезных функций для переговоров с людьми: ' +
                              'могу отвечать как на любое твоё сообщение, так и по команде; умею создавать мемы, ' +
                              'отправлять гифки, картинки и музыку на обозначенную тему.' + "\n" +
                              'Введите "/help", чтобы узнать больше о моих командах.',
                              reply_markup=ReplyKeyboardMarkup(KEYBOARD, one_time_keyboard=True))
