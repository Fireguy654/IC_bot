import json
import os
import random


def send_message(update, context):
    path = os.path.abspath(os.curdir)
    try:
        with open(path + '\\Data\\text.json', mode='r', encoding='utf-8') as file:
            text = json.load(file)
    except Exception:
        update.message.reply_text("Извините. Я пока ещё слишком мало знаю и не умею разговаривать :("
                                  "Поучусь ещё немного и будем беседовать")
        return
    if len(text) < 100:
        update.message.reply_text("Извините. Я пока ещё слишком мало знаю и не умею разговаривать :("
                                  "Поучусь ещё немного и будем беседовать")
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
