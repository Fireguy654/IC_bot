# Этот файл отвечает за изменение и сохранение настроек для конкретных диалогов.
# Настройки хранятся в файле Data/modes.json для предотвращения потерь данных при перезапуске бота.
from Functions.manipulate_mode_info import get_mode_info, dump_mode_info


# ch_study_mode - функция, принимающая на вход событие и окружение.
# Вызывается по команде /ch_study_mode.
# Изменяет режим обучения в конкретном диалоге.
# Значение True означает, что бот будет обучаться и отвечать, принимая информацию
# только от сообщений из этого диалога.
# False - из всех сообщений из диалогов со значением False в момент обработки.
# В момент получения сообщения бот записывает данные в зависимости от режима.
# Отвечает тоже в зависимости от него.
def ch_study_mode(update, context):
    chat_id = str(update.message.chat_id)
    info = get_mode_info()
    if chat_id not in info['study'].keys():
        info['study'][chat_id] = False
    info['study'][chat_id] = not info['study'][chat_id]
    dump_mode_info(info)
    if info['study'][chat_id]:
        update.message.reply_text('Режим обучения успешно изменён. Теперь бот будет обучаться и отвечать '
                                  'в диалоге с вами, основываясь только на ваших сообщениях.')
    else:
        update.message.reply_text('Режим обучения успешно изменён. Теперь бот будет обучаться и отвечать '
                                  'в диалоге с вами, основываясь на всех сообщениях.')


# ch_ans_mode - функция, принимающая на вход событие и окружение.
# Вызывается по команде /ch_answer_mode.
# Изменяет режим ответа в конкретном диалоге.
# Значение True означает, что будет отвечать на все текстовые сообщения пользователя,
# генерируя фразы.
# False - будет генерировать фразы только по команде.
def ch_ans_mode(update, context):
    chat_id = str(update.message.chat_id)
    info = get_mode_info()
    if chat_id not in info['answer'].keys():
        info['answer'][chat_id] = True
    info['answer'][chat_id] = not info['answer'][chat_id]
    dump_mode_info(info)
    if info['answer'][chat_id]:
        update.message.reply_text('Режим разговора успешно изменён. Теперь бот будет отвечать '
                                  'вам после ваших сообщений.')
    else:
        update.message.reply_text('Режим разговора успешно изменён. Теперь бот не будет отвечать '
                                  'вам после ваших сообшений.')
