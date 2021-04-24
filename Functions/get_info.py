import json
import os
from Functions.manipulate_mode_info import get_mode_info
from Functions.send_text import send_message


# get_info - функция, принимающая на вход событие и окружение.
# Принимает информацию из сообщений о словах и их связях между собой.
# Добавляет её в Data/text.json(Data/text<chat_id>.json если режим обучения равен True).
# Используется json для предотвращения потерь данных при перезапуске бота.
# Если режим ответа равен True, то вызывает функцию генерации фразы.
# Вызывается при текстовом сообщении.
def get_info(update, context):
    text = update.message.text
    if text[0] == '/':
        return
    chat_id = str(update.message.chat_id)
    info = get_mode_info()
    if chat_id not in info['study']:
        info['study'][chat_id] = False
    if chat_id not in info['answer']:
        info['answer'][chat_id] = True
    path = os.path.abspath(os.curdir)
    try:
        if info['study'][chat_id]:
            with open(path + '\\Data\\text' + chat_id + '.json', mode='r', encoding='utf-8') as file:
                words = json.load(file)
        else:
            with open(path + '\\Data\\text.json', mode='r', encoding='utf-8') as file:
                words = json.load(file)
    except Exception:
        words = {}
    text.replace(';', '.')
    last_t = '%'
    cur_t = ''
    try:
        for i in text:
            if i.isalpha() or cur_t != '' and i == '-':
                cur_t += i
            else:
                cur_t = cur_t.lower()
                if cur_t != '':
                    if cur_t == '' or last_t == '':
                        raise ValueError(f'Cur token: {cur_t}. Last_t: {last_t}.')
                    if last_t not in words:
                        words[last_t] = {}
                    if cur_t in words[last_t]:
                        words[last_t][cur_t] = str(int(words[last_t][cur_t]) + 1)
                    else:
                        words[last_t][cur_t] = '1'
                if i in ['.', '!', '?']:
                    if cur_t != '':
                        last_t = cur_t
                        cur_t = ''
                    if last_t == '%':
                        continue
                    cur_t = '%'
                    if cur_t == '' or last_t == '':
                        raise ValueError(f'Cur token: {cur_t}. Last_t: {last_t}.')
                    if last_t not in words:
                        words[last_t] = {}
                    if cur_t in words[last_t]:
                        words[last_t][cur_t] = str(int(words[last_t][cur_t]) + 1)
                    else:
                        words[last_t][cur_t] = '1'
                    last_t = cur_t
                    cur_t = ''
                else:
                    if cur_t != '':
                        last_t = cur_t
                        cur_t = ''
        cur_t = cur_t.lower()
        if cur_t != '':
            if cur_t == '' or last_t == '':
                raise ValueError(f'Cur token: {cur_t}. Last_t: {last_t}.')
            if last_t not in words:
                words[last_t] = {}
            if cur_t in words[last_t]:
                words[last_t][cur_t] = str(int(words[last_t][cur_t]) + 1)
            else:
                words[last_t][cur_t] = '1'
            last_t = cur_t
        if last_t != '%':
            cur_t = '%'
            if cur_t == '' or last_t == '':
                raise ValueError(f'Cur token: {cur_t}. Last_t: {last_t}.')
            if last_t not in words:
                words[last_t] = {}
            if cur_t in words[last_t]:
                words[last_t][cur_t] = str(int(words[last_t][cur_t]) + 1)
            else:
                words[last_t][cur_t] = '1'
    except ValueError as e:
        print(e)
    path = os.path.abspath(os.curdir)
    if info['study'][chat_id]:
        with open(path + '\\Data\\text' + chat_id + '.json', mode='w', encoding='utf-8') as file:
            json.dump(words, file, ensure_ascii=False)
    else:
        with open(path + '\\Data\\text.json', mode='w', encoding='utf-8') as file:
            json.dump(words, file, ensure_ascii=False)
    if info['answer'][chat_id]:
        send_message(update, context)
