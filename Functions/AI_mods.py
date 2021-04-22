from Functions.manipulate_mode_info import get_mode_info, dump_mode_info


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
