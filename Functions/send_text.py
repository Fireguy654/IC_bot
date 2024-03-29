import json
import os
import random
from Functions.manipulate_mode_info import get_mode_info


# send_message - функция, принимающая на вход событие и окружение.
# Вызывается по команде /something.
# Также может вызываться из get_info, если режим ответа равен True.
# Берёт информацию о связях слов из
# Data/text.json(Data/text<chat_id>.json если режим обучения равен True).
# Генерирует фразу: на каждом слове берёт рандомное из топ-10 используемых по связям слов.
# И отправляет фразу в диалог.
def send_message(update, context):
    path = os.path.abspath(os.curdir)
    info = get_mode_info()
    chat_id = str(update.message.chat_id)
    if chat_id not in info['study']:
        info['study'][chat_id] = False
    try:
        if info['study'][chat_id]:
            with open(path + '\\Data\\text' + chat_id + '.json', mode='r', encoding='utf-8') as file:
                text = json.load(file)
        else:
            with open(path + '\\Data\\text.json', mode='r', encoding='utf-8') as file:
                text = json.load(file)
    except Exception:
        update.message.reply_text("Извините. Я пока ещё слишком мало знаю и не умею разговаривать :("
                                  " Поучусь ещё немного и будем беседовать")
        return
    if len(text) < 100:
        update.message.reply_text("Извините. Я пока ещё слишком мало знаю и не умею разговаривать :("
                                  " Поучусь ещё немного и будем беседовать")
        return
    sent = random.randint(1, 10)
    ans = []
    for i in range(sent):
        cur = []
        tokens = random.randint(10, 20)
        last = '%'
        while True:
            if tokens == 0:
                if '%' in text[last]:
                    break
                else:
                    tmp = list(text[last].keys())
                    tmp.sort(key=lambda x: int(text[last][x]))
                    last = random.choice(tmp[:10])
                    cur.append(last)
                continue
            tmp = list(text[last].keys())
            tmp.sort(key=lambda x: int(text[last][x]))
            if len(tmp) == 1 and tmp[0] == '%':
                break
            tmp = tmp[:10]
            token = random.choice(tmp)
            while token == '%':
                token = random.choice(tmp)
            cur.append(token)
            last = token
            tokens -= 1
        ans.append(' '.join(cur).capitalize())
    update.message.reply_text('. '.join(ans))
