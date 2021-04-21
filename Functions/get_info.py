import json
import os


def get_info(update, context):
    path = os.path.abspath(os.curdir)
    try:
        with open(path + '\\Data\\text.json', mode='r', encoding='utf-8') as file:
            words = json.load(file)
    except Exception:
        words = {}
    text = update.message.text
    if text[0] == '/':
        return
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
    with open(path + '\\Data\\text.json', mode='w', encoding='utf-8') as file:
        json.dump(words, file, ensure_ascii=False)
